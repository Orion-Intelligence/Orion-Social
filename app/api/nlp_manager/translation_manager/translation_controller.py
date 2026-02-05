from pathlib import Path
import warnings
from langdetect import detect, DetectorFactory
import argostranslate.package
import argostranslate.translate

DetectorFactory.seed = 0

class translation_controller:

    def initialize(self):
        self._install_local_models()
        argostranslate.translate.load_installed_languages()
        self._load_installed_languages()

    @staticmethod
    def _install_local_models():
        local_model_dir = Path(__file__).resolve().parent.parent.parent.parent / "raw/translation"
        local_model_dir = local_model_dir.resolve()
        for file_path in local_model_dir.iterdir():
            try:
                argostranslate.package.install_from_path(file_path)
            except Exception as ex:
                warnings.warn(f"[WARNING] Failed to install model {file_path.name}: {ex}")

    def _load_installed_languages(self):
        self.translators = {}
        self.installed_languages = argostranslate.translate.get_installed_languages()
        self.en_lang = next((lang for lang in self.installed_languages if lang.code == "en"), None)
        self.ru_lang = next((lang for lang in self.installed_languages if lang.code == "ru"), None)
        self.zh_lang = next((lang for lang in self.installed_languages if lang.code == "zh"), None)
        self.ar_lang = next((lang for lang in self.installed_languages if lang.code == "ar"), None)
        if not self.en_lang:
            raise RuntimeError("English language model is not installed.")
        if not self.ru_lang or not self.zh_lang or not self.ar_lang:
            raise RuntimeError("Required language models (ru, zh, ar) are not all installed.")
        self.translators = {
            "ru": self.ru_lang.get_translation(self.en_lang),
            "uk": self.ru_lang.get_translation(self.en_lang),
            "be": self.ru_lang.get_translation(self.en_lang),
            "bg": self.ru_lang.get_translation(self.en_lang),
            "mk": self.ru_lang.get_translation(self.en_lang),
            "zh": self.zh_lang.get_translation(self.en_lang),
            "ar": self.ar_lang.get_translation(self.en_lang),
        }

    def translate(self, text):
        try:
            if not text or not text.strip():
                return text
            lang = detect(text)
            if lang == "en":
                return text
            translation = text
            if lang in {"ru", "uk", "be", "bg", "mk"} :
                translation = self.translators['ru'].translate(text)
            if lang in {"ar"}:
                translation = self.translators['ar'].translate(text)
            if lang in {"zh", "zh-cn"}:
                translation = self.translators['zh'].translate(text)
            return translation
        except Exception as ex:
            warnings.warn(f"[ERROR] Translation failed: {ex}")
            return text