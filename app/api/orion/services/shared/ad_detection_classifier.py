import os
import threading
from typing import Literal
from pydantic import BaseModel

class AdDetectionResult(BaseModel):
    topic: str
    confidence: float
    model: str

class AdDetectionClassifier:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AdDetectionClassifier, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        
        with self._lock:
            if getattr(self, "_initialized", False):
                return
            self._initialized = False
            self.model_name = os.getenv("AD_DETECTION_MODEL", "MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
            self.ad_threshold = float(os.getenv("AD_DETECTION_THRESHOLD", "0.5"))
            self.timeout = float(os.getenv("AD_DETECTION_TIMEOUT", "15.0"))
            self.classifier = None
            self.executor = None

    def load(self):
        if getattr(self, "_initialized", False):
            return
        
        with self._lock:
            if self._initialized:
                return
            
            from transformers import pipeline
            import os
            import time
            import logging
            import json
            import concurrent.futures
            
            start_time = time.time()
            self.model_name = os.getenv("AD_DETECTION_MODEL", "MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
            
            try:
                self.classifier = pipeline(
                    "zero-shot-classification", 
                    model=self.model_name, 
                    device=-1,
                    truncation=True,
                    max_length=512
                )
                self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
                load_time_ms = (time.time() - start_time) * 1000
                logging.debug(json.dumps({
                    "event": "model_loaded",
                    "model": self.model_name,
                    "latency_ms": round(load_time_ms, 2)
                }))
            except Exception as e:
                self.classifier = None
                self.executor = None
                logging.error(json.dumps({
                    "event": "model_init_failed",
                    "model": self.model_name,
                    "error": str(e)
                }))
            
            self._initialized = True

    def classify(self, text: str) -> AdDetectionResult:
        if getattr(self, "model_name", None) is None or getattr(self, "classifier", None) is None:
            return AdDetectionResult(topic="Unknown", confidence=0.0, model=getattr(self, "model_name", "unknown"))
            
        if not text or not str(text).strip():
            return AdDetectionResult(topic="Unknown", confidence=0.0, model=self.model_name)
        
        text = str(text).strip()
        candidate_labels = ["Technology", "Finance", "Fashion", "Health", "Food", "Entertainment", "Sports", "Other"]
        
        try:
            import time
            import logging
            import json
            import concurrent.futures
            start_time = time.time()
            
            if self.executor is None:
                raise RuntimeError("Executor is not initialized")
                
            future = self.executor.submit(self.classifier, text, candidate_labels)
            try:
                results = future.result(timeout=self.timeout)
            except concurrent.futures.TimeoutError:
                logging.error(json.dumps({
                    "event": "inference_timeout",
                    "model": self.model_name,
                    "latency_ms": round((time.time() - start_time) * 1000, 2)
                }))
                return AdDetectionResult(
                    topic="Unknown",
                    confidence=0.0,
                    model=self.model_name
                )
            
            inference_time_ms = (time.time() - start_time) * 1000
            
            top_label = results['labels'][0]
            top_score = results['scores'][0]
            
            result = AdDetectionResult(
                topic=top_label,
                confidence=top_score,
                model=self.model_name
            )
                
            logging.debug(json.dumps({
                "event": "inference_completed",
                "model": self.model_name,
                "latency_ms": round(inference_time_ms, 2),
                "topic": result.topic,
                "confidence": round(result.confidence, 4)
            }))
            return result
                
        except Exception as e:
            import logging
            import json
            logging.error(json.dumps({
                "event": "inference_failed",
                "model": getattr(self, "model_name", "unknown"),
                "error": str(e)
            }))
            return AdDetectionResult(
                topic="Unknown",
                confidence=0.0,
                model=getattr(self, "model_name", "unknown")
            )

ad_detection_classifier = AdDetectionClassifier()
