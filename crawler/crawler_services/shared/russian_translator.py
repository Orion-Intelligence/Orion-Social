import hashlib
import re
import shutil
import subprocess

from crawler.crawler_services.log_manager.log_controller import log


class russian_translator:
    DICT_DATABASE = "freedict-rus-eng"
    APT_PACKAGES = ("dict", "dictd", "dict-freedict-rus-eng")
    PHRASE_GLOSSARY = {
        "база данных": "database",
        "базы данных": "databases",
        "взлом базы данных": "database breach",
        "компрометация сервера": "server compromise",
        "магазин аккаунтов": "account shop",
        "продажа аккаунтов": "account sales",
        "куплю не сильно дорого": "will buy not too expensive",
        "мир танков": "World of Tanks",
        "перехват смс": "SMS interception",
        "перехват уведомлений": "notification interception",
        "смс и уведомлений": "SMS and notifications",
        "кто на самом деле стоял за": "who was really behind",
        "кто стоит за": "who is behind",
        "криптовалютной аферой": "cryptocurrency scam",
        "это мошенник или нет": "is this a scammer or not",
        "правительство китая": "Chinese government",
        "финансирует хакерские атаки": "funds hacker attacks",
        "криптовалютные биржи": "cryptocurrency exchanges",
        "не покупайте ничего": "do not buy anything",
        "помогаю с верификацией": "help with verification",
        "редактирование, фотошоп": "editing, photoshop",
        "верификация kyc": "KYC verification",
        "разблокировка аккаунтов": "account unlocking",
        "разблокировкой аккаунтов": "account unlocking",
        "без предоплат": "no prepayment",
        "отрисовщик чеков": "receipt generator",
    }
    WORD_GLOSSARY = {
        "аккаунт": "account",
        "аккаунта": "account",
        "аккаунтов": "accounts",
        "аккаунты": "accounts",
        "атака": "attack",
        "атаки": "attacks",
        "аферой": "scam",
        "база": "database",
        "базы": "databases",
        "бесплатно": "free",
        "биржи": "exchanges",
        "ботнет": "botnet",
        "взлом": "hack",
        "взлома": "hack",
        "верификацией": "verification",
        "вирус": "virus",
        "вирусы": "viruses",
        "данных": "data",
        "доступ": "access",
        "загрузчик": "loader",
        "китая": "China",
        "криптовалютной": "cryptocurrency",
        "криптовалютные": "cryptocurrency",
        "крупнейшей": "largest",
        "майнер": "miner",
        "медиа": "media",
        "модульный": "modular",
        "мошенник": "scammer",
        "ничего": "nothing",
        "письма": "emails",
        "писем": "emails",
        "покупайте": "buy",
        "перехват": "interception",
        "проверяйте": "check",
        "правительство": "government",
        "пробив": "lookup",
        "продажа": "sale",
        "разблокировкой": "unlocking",
        "резидентный": "resident",
        "скрин": "screenshot",
        "скринов": "screenshots",
        "скачать": "download",
        "стиллер": "stealer",
        "стоял": "stood",
        "стоит": "stands",
        "сервер": "server",
        "сервера": "server",
        "смс": "SMS",
        "сми": "media",
        "троян": "trojan",
        "трояны": "trojans",
        "уведомлений": "notifications",
        "укрпошта": "Ukrposhta",
        "файлы": "files",
        "финансирует": "funds",
        "хакерские": "hacker",
        "черви": "worms",
        "чеков": "receipts",
        "в": "in",
        "года": "of the year",
        "за": "behind",
        "и": "and",
        "или": "or",
        "на": "on",
        "с": "with",
    }

    _checked = False
    _available = False
    _cache: dict[str, str] = {}
    _word_cache: dict[str, str | None] = {}

    @classmethod
    def has_russian(cls, text: str | None) -> bool:
        return any("\u0400" <= char <= "\u04ff" for char in text or "")

    @classmethod
    def translate(cls, text: str | None, auto_install: bool = True) -> str:
        if not text:
            return ""
        if not cls.has_russian(text):
            return text

        cache_key = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        if not cls._is_available() and auto_install:
            cls._install()

        if not cls._is_available():
            translated = cls._fallback_translate(text)
            cls._cache[cache_key] = translated
            return translated

        translated = cls._translate_words(text)
        if translated == text:
            translated = cls._fallback_translate(text)
        cls._cache[cache_key] = translated
        return translated

    @classmethod
    def forum_title(cls, text: str | None) -> str:
        if not text:
            return ""
        if not cls.has_russian(text):
            return text
        if cls._has_title_translation_prefix(text):
            return text

        translated = cls.translate(text, auto_install=False)
        if not translated or translated == text:
            return text
        return f"{translated}: {text}"

    @classmethod
    def forum_content(cls, text: str | None, preview_lines: int = 2) -> str:
        if not text:
            return ""
        if not cls.has_russian(text):
            return text
        if cls._has_content_translation_prefix(text, preview_lines):
            return text

        lines = text.splitlines()
        preview = []
        for line in lines:
            value = line.strip()
            if not value:
                continue
            preview.append(value)
            if len(preview) >= preview_lines:
                break

        preview_text = "\n".join(preview)
        if not cls.has_russian(preview_text):
            return text

        translated = cls.translate(preview_text, auto_install=False)
        if not translated or translated == preview_text:
            return text
        return f"{translated}:\n{text}"

    @classmethod
    def _has_title_translation_prefix(cls, text: str) -> bool:
        for match in re.finditer(r":\s+", text):
            translated = text[:match.start()].strip()
            original = text[match.end():].strip()
            if translated and original and not cls.has_russian(translated) and cls.has_russian(original):
                if cls.translate(original, auto_install=False).strip() == translated:
                    return True
        return False

    @classmethod
    def _has_content_translation_prefix(cls, text: str, preview_lines: int) -> bool:
        for match in re.finditer(r":\n", text):
            translated = text[:match.start()].strip()
            original = text[match.end():].strip()
            if not translated or not original or cls.has_russian(translated) or not cls.has_russian(original):
                continue

            preview = []
            for line in original.splitlines():
                value = line.strip()
                if not value:
                    continue
                preview.append(value)
                if len(preview) >= preview_lines:
                    break
            if preview and cls.translate("\n".join(preview), auto_install=False).strip() == translated:
                return True
        return False

    @classmethod
    def _is_available(cls) -> bool:
        if cls._checked:
            return cls._available

        cls._checked = True
        if shutil.which("dict") is None:
            cls._available = False
            return False

        try:
            result = subprocess.run(
                ["dict", "-D"],
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )
            cls._available = cls.DICT_DATABASE in result.stdout
        except Exception:
            cls._available = False

        return cls._available

    @classmethod
    def _install(cls) -> None:
        cls._checked = False
        if shutil.which("apt-get") is None or shutil.which("sudo") is None:
            return

        try:
            subprocess.check_call(["sudo", "-n", "apt-get", "install", "-y", *cls.APT_PACKAGES])
        except Exception as ex:
            log.g().w(f"Could not auto-install Russian translator packages: {ex}")

    @classmethod
    def _translate_words(cls, text: str) -> str:
        return re.sub(r"[\u0400-\u04ff]+(?:-[\u0400-\u04ff]+)?", cls._translate_word, text)

    @classmethod
    def _fallback_translate(cls, text: str) -> str:
        translated = text
        for phrase, replacement in sorted(cls.PHRASE_GLOSSARY.items(), key=lambda item: len(item[0]), reverse=True):
            translated = re.sub(re.escape(phrase), replacement, translated, flags=re.IGNORECASE)
        return re.sub(r"[\u0400-\u04ff]+(?:-[\u0400-\u04ff]+)?", cls._fallback_word, translated)

    @classmethod
    def _fallback_word(cls, match: re.Match[str]) -> str:
        word = match.group(0)
        return cls.WORD_GLOSSARY.get(word.lower(), word)

    @classmethod
    def _translate_word(cls, match: re.Match[str]) -> str:
        word = match.group(0)
        key = word.lower()
        if key not in cls._word_cache:
            cls._word_cache[key] = cls._lookup_word(key)
        return cls._word_cache[key] or word

    @classmethod
    def _lookup_word(cls, word: str) -> str | None:
        try:
            result = subprocess.run(
                ["dict", "-d", cls.DICT_DATABASE, word],
                text=True,
                capture_output=True,
                timeout=5,
                check=False,
            )
        except Exception as ex:
            log.g().w(f"Russian translation failed: {ex}")
            return None

        if result.returncode != 0:
            return None

        return cls._parse_dict_output(result.stdout, word)

    @classmethod
    def _parse_dict_output(cls, output: str, word: str) -> str | None:
        for line in output.splitlines():
            value = line.strip()
            if not value:
                continue
            lower = value.lower()
            if lower == word or lower.startswith(("from ", "data for ", "no definitions", "no match")):
                continue
            if " definition" in lower or lower.startswith(cls.DICT_DATABASE):
                continue

            value = re.sub(r"^\d+[\).]\s*", "", value)
            value = re.split(r"[;,]", value, maxsplit=1)[0].strip()
            if value and not cls.has_russian(value):
                return value
        return None
