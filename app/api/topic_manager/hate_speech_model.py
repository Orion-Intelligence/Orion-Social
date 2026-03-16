import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class hate_speech_model:

    def __init__(self):
        self.model_name = "facebook/roberta-hate-speech-dynabench-r4-target"
        logger.info(f"Loading hate speech model: {self.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.model.eval()

    def predict(self, text: str) -> dict:
        if not text or not text.strip():
            return {"label": "nothate", "score": 1.0}

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=-1).item()
        score = probabilities[0][predicted_class].item()

        # Model labels: 0 = nothate, 1 = hate
        label = "hate" if predicted_class == 1 else "nothate"

        return {"label": label, "score": round(score, 4)}
