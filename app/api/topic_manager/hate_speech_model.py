import logging
from pathlib import Path

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MODEL_ID = "mrm8488/distilroberta-finetuned-tweets-hate-speech"
LOCAL_MODEL_DIR = (
    Path(__file__).resolve().parents[2]
    / "raw"
    / "model"
    / "hate_speech"
    / "mrm8488_distilroberta_finetuned_tweets_hate_speech"
)


class hate_speech_model:

    def __init__(self):
        self._cache_model_if_missing()
        self.model = pipeline(
            "text-classification",
            model=str(LOCAL_MODEL_DIR),
            tokenizer=str(LOCAL_MODEL_DIR),
            local_files_only=True,
        )

    def _cache_model_if_missing(self) -> None:
        if (LOCAL_MODEL_DIR / "config.json").exists() and (LOCAL_MODEL_DIR / "tokenizer_config.json").exists():
            return

        logger.info("Local cache missing. Downloading hate speech model: %s", MODEL_ID)
        LOCAL_MODEL_DIR.mkdir(parents=True, exist_ok=True)

        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)

        tokenizer.save_pretrained(LOCAL_MODEL_DIR)
        model.save_pretrained(LOCAL_MODEL_DIR)
        logger.info("Hate speech model cached at: %s", LOCAL_MODEL_DIR)

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
            return {"is_hate": False}

        result = self.model(text, truncation=True)[0]
        predicted_label = result.get("label", "")
        is_hate = self._is_hate_label(predicted_label)

        return {"is_hate": is_hate}
