import os
import threading
from typing import Literal
from pydantic import BaseModel

class HateSpeechResult(BaseModel):
    is_hate_speech: bool
    label: Literal["safe", "offensive", "hate_speech", "unknown"]
    confidence: float
    explanation: str | None = None
    model: str

class HateSpeechClassifier:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(HateSpeechClassifier, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        
        with self._lock:
            if getattr(self, "_initialized", False):
                return
            self._initialized = False
            self.model_name = os.getenv("HATE_SPEECH_MODEL", "unitary/toxic-bert")
            self.hate_threshold = float(os.getenv("HATE_SPEECH_THRESHOLD", "0.5"))
            self.offensive_threshold = float(os.getenv("OFFENSIVE_THRESHOLD", "0.5"))
            self.timeout = float(os.getenv("HATE_SPEECH_TIMEOUT", "2.0"))
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
            start_time = time.time()
            
            self.model_name = os.getenv("HATE_SPEECH_MODEL", "unitary/toxic-bert")
            
            import concurrent.futures
            
            try:
                self.classifier = pipeline(
                    "text-classification", 
                    model=self.model_name, 
                    tokenizer=self.model_name,
                    device=-1, 
                    return_all_scores=True,
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

    def classify(self, text: str) -> HateSpeechResult:
        if getattr(self, "model_name", None) is None or getattr(self, "classifier", None) is None:
            return HateSpeechResult(is_hate_speech=False, label="unknown", confidence=0.0, explanation="Classifier not initialized", model=getattr(self, "model_name", "unknown"))
            
        if not text or not str(text).strip():
            return HateSpeechResult(is_hate_speech=False, label="safe", confidence=1.0, explanation="Empty text", model=self.model_name)
        
        text = str(text).strip()
        
        try:
            import time
            import logging
            import json
            import concurrent.futures
            start_time = time.time()
            
            if self.executor is None:
                raise RuntimeError("Executor is not initialized")
                
            future = self.executor.submit(self.classifier, text)
            try:
                results = future.result(timeout=self.timeout)[0]
            except concurrent.futures.TimeoutError:
                logging.error(json.dumps({
                    "event": "inference_timeout",
                    "model": self.model_name,
                    "latency_ms": round((time.time() - start_time) * 1000, 2)
                }))
                return HateSpeechResult(
                    is_hate_speech=False,
                    label="unknown",
                    confidence=0.0,
                    explanation=f"Classification timed out after {self.timeout}s",
                    model=self.model_name
                )
            
            inference_time_ms = (time.time() - start_time) * 1000
            
            scores = {res['label']: res['score'] for res in results}
            
            hate_score = max(scores.get('identity_hate', 0.0), scores.get('threat', 0.0), scores.get('severe_toxic', 0.0))
            offensive_score = max(scores.get('toxic', 0.0), scores.get('obscene', 0.0), scores.get('insult', 0.0))
            
            hate_threshold = self.hate_threshold
            offensive_threshold = self.offensive_threshold
            
            if hate_score >= hate_threshold:
                result = HateSpeechResult(
                    is_hate_speech=True,
                    label="hate_speech",
                    confidence=hate_score,
                    explanation="Detected severe toxicity, threats, or identity hate.",
                    model=self.model_name
                )
            elif offensive_score >= offensive_threshold:
                result = HateSpeechResult(
                    is_hate_speech=False,
                    label="offensive",
                    confidence=offensive_score,
                    explanation="Detected toxicity, obscenity, or insults.",
                    model=self.model_name
                )
            else:
                safe_confidence = 1.0 - max(hate_score, offensive_score)
                result = HateSpeechResult(
                    is_hate_speech=False,
                    label="safe",
                    confidence=safe_confidence,
                    explanation="No significant toxicity detected.",
                    model=self.model_name
                )
                
            logging.debug(json.dumps({
                "event": "inference_completed",
                "model": self.model_name,
                "latency_ms": round(inference_time_ms, 2),
                "label": result.label,
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
            return HateSpeechResult(
                is_hate_speech=False, 
                label="unknown", 
                confidence=0.0, 
                explanation=f"Classification failed: {str(e)}",
                model=getattr(self, "model_name", "unknown")
            )

hate_speech_classifier = HateSpeechClassifier()
