from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class hate_speech_model:

    def __init__(self):
        self.model = pipeline(
            "text-classification",
            model="TaiwoOgun/minilm-hate-speech",
        )

    @staticmethod
    def _is_hate_label(raw_label: str) -> bool:
        label = (raw_label or "").strip().lower().replace("_", "-")
        if label in {"hate", "label-1", "toxic", "offensive"}:
            return True
        if label in {"nothate", "non-hate", "not-hate", "label-0"}:
            return False
        return "hate" in label and "non" not in label and "not" not in label

    def predict(self, text: str) -> dict:
        if not text or not text.strip():
            return {"label": "nothate", "score": 1.0}

        result = self.model(text, truncation=True)[0]
        predicted_label = result.get("label", "")
        predicted_score = float(result.get("score", 0.0))

        is_hate = self._is_hate_label(predicted_label)
        toxicity = predicted_score if is_hate else (1.0 - predicted_score)

        label = "hate" if is_hate else "nothate"

        return {"label": label, "score": round(toxicity, 4)}
