from datetime import datetime, timedelta
from typing import Optional, List
from urllib.parse import urlunparse

import requests
from bs4 import BeautifulSoup

import json
import os
import re
import zipfile
import socket
import base64
import hashlib

from crawler.crawler_instance.genbot_service.shared.shared_data_controller import shared_data_controller
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_services.log_manager.log_controller import log
from urllib.parse import urlparse
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.redis_manager.redis_enums import REDIS_KEYS, REDIS_COMMANDS

HTTP_SCHEME = "http" + "://"

STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'if', 'while', 'with', 'at', 'by', 'for',
    'from', 'into', 'on', 'of', 'to', 'in', 'out', 'over', 'under', 'above', 'below',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
    'does', 'did', 'can', 'could', 'should', 'would', 'may', 'might', 'must', 'will',
    'shall', 'not', 'no', 'nor', 'this', 'that', 'these', 'those', 'it', 'its', 'i',
    'you', 'he', 'she', 'we', 'they', 'them', 'me', 'my', 'your', 'his', 'her', 'our',
    'their', 'as', 'so', 'than', 'too', 'very', 'has', 'the', 'for'
}


class helper_method:

    @staticmethod
    def scalar_text(value: object | None) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, (int, float, bool)):
            return str(value)
        return ""

    @staticmethod
    def clean_summary(text: str, max_length: int = 300) -> str:
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'[\s\t\n\r]+', ' ', text)
        text = text.strip()
        return text[:max_length]

    @staticmethod
    def parse_date(date_str):
        if not date_str:
            return None

        if date_str.lower().strip() == "just now":
            return datetime.now()

        m = re.match(r"(\d+)\s+minute[s]?\s+ago", date_str, re.IGNORECASE)
        if m:
            minutes = int(m.group(1))
            return datetime.now() - timedelta(minutes=minutes)

        h = re.match(r"(\d+)\s+hour[s]?\s+ago", date_str, re.IGNORECASE)
        if h:
            hours = int(h.group(1))
            return datetime.now() - timedelta(hours=hours)

        d = re.match(r"(\d+)\s+day[s]?\s+ago", date_str, re.IGNORECASE)
        if d:
            days = int(d.group(1))
            return datetime.now() - timedelta(days=days)

        if date_str.startswith("Yesterday at "):
            try:
                t = datetime.strptime(date_str[13:], "%I:%M %p").time()
                y = datetime.now()
                return datetime.combine((y - timedelta(days=1)).date(), t)
            except:
                pass

        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in weekdays:
            if date_str.startswith(day + " at "):
                try:
                    t = datetime.strptime(date_str[len(day) + 4:], "%I:%M %p").time()
                    today = datetime.now()
                    target_weekday = weekdays.index(day)
                    days_diff = (today.weekday() - target_weekday) % 7
                    target_date = today - timedelta(days=days_diff)
                    return datetime.combine(target_date.date(), t)
                except:
                    pass

        ds = re.sub(r'(\b\d{1,2})(st|nd|rd|th)\b', r'\1', date_str)
        for fmt in ("%b %d, %Y", "%B %d, %Y"):
            try:
                return datetime.strptime(ds, fmt)
            except ValueError:
                pass

        iso_like = (
                re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", date_str) or
                re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", date_str)
        )
        if iso_like:
            try:
                if "Z" in date_str:
                    date_str = date_str.replace("Z", "+00:00")
                date_str = re.sub(r'([+-]\d{2})(\d{2})$', r'\1:\2', date_str)
                return datetime.fromisoformat(date_str)
            except:
                pass

        return None

    @staticmethod
    def filter_comments(s: str) -> str:
        s = s.strip()
        if not s:
            return ""
        words = s.split()
        if len(words) < 4:
            return ""
        return s

    @staticmethod
    def generate_data_hash(data):
        if isinstance(data, dict):
            data_copy = {key: value for key, value in data.items() if
                         key not in {'m_update_date', 'm_base_url', 'm_url'}}
            data_string = json.dumps(data_copy, sort_keys=True)
        elif isinstance(data, str):
            data_string = data
        else:
            raise ValueError("Input must be a dictionary or a string")

        return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

    @staticmethod
    def get_base_url(url):
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return base_url

    @staticmethod
    def is_stop_word(p_word):
        if p_word in STOPWORDS:
            return True
        else:
            return False

    @staticmethod
    def extract_entities(pairs: List[tuple[str, entity_model]]) -> List[entity_model]:
        texts = [text for text, _ in pairs]
        results = shared_data_controller.get_instance().trigger_nlp_classifier(texts)

        updated_models = []
        for (text, model), result in zip(pairs, results):
            entity_fields = getattr(model.__class__, "model_fields", getattr(model.__class__, "__fields__", {}))
            for entry in result:
                for key, value in entry.items():
                    if key in {"m_domains", "m_file_path"} or key not in entity_fields or not value:
                        continue
                    existing = getattr(model, key, [])
                    if not isinstance(existing, list):
                        existing = []
                    if isinstance(value, str):
                        if value not in existing:
                            existing.append(value)
                    elif isinstance(value, list):
                        existing.extend([v for v in value if v not in existing])
                    setattr(model, key, existing)
            updated_models.append(model)

        return updated_models

    @staticmethod
    def strip_special_character(p_text):
        m_text = re.sub(r"^\W+", "", p_text)
        return m_text

    @staticmethod
    def on_clean_url(p_url):
        parsed_url = urlparse(p_url)
        netloc = parsed_url.netloc.replace("www.", "", 1)
        cleaned_url = urlunparse((
            parsed_url.scheme,
            netloc.lower(),
            parsed_url.path.rstrip('/ '),
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment
        ))
        return cleaned_url

    @staticmethod
    def extract_and_convert_date(text: str) -> Optional[datetime.date]:
        for pattern, fmt in [
            (r'(\d{4}-\d{2}-\d{2})', "%Y-%m-%d"),
            (r'(\d{4}/\d{2}/\d{2})', "%Y/%m/%d"),
            (r'(\d{2}-\d{2}-\d{4})', "%d-%m-%Y"),
            (r'(\d{2}/\d{2}/\d{4})', "%m/%d/%Y"),
            (r'(\d{1,2} \w+ \d{4})', "%d %B %Y")
        ]:
            if match := re.search(pattern, text):
                try:
                    return datetime.strptime(match.group(0), fmt).date()
                except ValueError:
                    continue
        return None

    @staticmethod
    def remove_stopwords_from_string(text: str) -> str:
        additional_stopwords = {
            "was", "by", "were", "been", "being", "have", "has", "had", "do", "does", "did",
            "will", "would", "shall", "should", "may", "might", "can", "could", "must",
            "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "them",
            "my", "your", "his", "its", "our", "their", "mine", "yours", "hers", "ours", "theirs",
            "this", "that", "these", "those", "here", "there", "where", "when", "why", "how",
            "also", "just", "still", "even", "yet", "so", "than", "then", "very", "too",
            "because", "while", "though", "although", "if", "unless", "until", "before", "after",
            "once", "again", "ever", "always", "sometimes", "often", "never", "each", "every",
            "any", "all", "some", "no", "none", "both", "either", "neither", "few", "several",
            "many", "much", "most", "more", "less", "lot", "lots", "such",
            "get", "got", "gets", "getting", "make", "makes", "made", "say", "says", "said",
            "go", "goes", "went", "gone", "see", "sees", "saw", "seen", "know", "knows", "knew", "known",
            "take", "takes", "took", "taken", "come", "comes", "came", "coming",
            "thing", "things", "something", "anything", "everything", "nothing"
        }

        tokens = re.findall(r'\b\w+\b', text)
        filtered_tokens = [word for word in tokens if word.lower() not in additional_stopwords]
        return ' '.join(filtered_tokens)

    @staticmethod
    def extract_refhtml(url: str, invoke_db, REDIS_COMMANDS, CUSTOM_SCRIPT_REDIS_KEYS, RAW_PATH_CONSTANTS, page) -> str | None:
        if url is None:
            return None

        if not url.startswith("http"):
            url = f"https://{url.removeprefix(HTTP_SCHEME).removeprefix('https://')}"
        if not helper_method.is_valid_url(url):
            return None

        redis_key = CUSTOM_SCRIPT_REDIS_KEYS.URL_PARSED.value + url
        is_crawled = int(invoke_db(REDIS_COMMANDS.S_GET_INT, redis_key, 0, RAW_PATH_CONSTANTS.HREF_TIMEOUT))
        if is_crawled == -1 or is_crawled >= 5:
            return None

        try:
            resp = requests.get(url, timeout=20, allow_redirects=True)
            if 400 <= (resp.status_code or 0) < 600:
                raise RuntimeError(f"bad status: {resp.status_code}")

            parts = []
            soup = BeautifulSoup(resp.text, "html.parser")
            title_text = soup.title.string if soup.title and soup.title.string else ""
            if title_text.strip():
                parts.append(title_text.strip())
            el = soup.find("meta", attrs={"name": "description"})
            desc = el.get("content") if el and el.get("content") else None
            if desc and desc.strip():
                parts.append(desc.strip())
            for e in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
                t = e.get_text(strip=True)
                if t and t.strip():
                    parts.append(t.strip())

            result, total = [], 0
            for part in filter(None, parts):
                total += len(part) + (3 if result else 0)
                result.append(part)
                if total > 1500:
                    break

            text = " - ".join(result)[:2000] or None
            if text:
                invoke_db(REDIS_COMMANDS.S_SET_INT, redis_key, -1, RAW_PATH_CONSTANTS.HREF_TIMEOUT)
            else:
                invoke_db(REDIS_COMMANDS.S_SET_INT, redis_key, is_crawled + 1, RAW_PATH_CONSTANTS.HREF_TIMEOUT)
            return text[:1000] if text else None
        except Exception as _:
            return None

    @staticmethod
    def extract_refhtml_requests(url: str, invoke_db, REDIS_COMMANDS, CUSTOM_SCRIPT_REDIS_KEYS, RAW_PATH_CONSTANTS, session) -> str | None:
        if url is None:
            return None
        if not url.startswith("http"):
            url = f"https://{url.lstrip(HTTP_SCHEME).lstrip('https://')}"
        if not helper_method.is_valid_url(url):
            return None
        redis_key = CUSTOM_SCRIPT_REDIS_KEYS.URL_PARSED.value + url
        is_crawled = int(invoke_db(REDIS_COMMANDS.S_GET_INT, redis_key, 0, RAW_PATH_CONSTANTS.HREF_TIMEOUT))
        if is_crawled == -1 or is_crawled >= 5:
            return None
        try:
            resp = session.get(url, timeout=20, allow_redirects=True)
            resp.raise_for_status()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")
            parts = []
            title_text = (soup.title.string if soup.title and soup.title.string else "")
            if title_text.strip():
                parts.append(title_text.strip())
            el = soup.find("meta", attrs={"name": "description"})
            desc = el.get("content") if el and el.get("content") else None
            if desc and desc.strip():
                parts.append(desc.strip())
            for e in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
                t = e.get_text(strip=True)
                if t:
                    parts.append(t)
            result, total = [], 0
            for part in filter(None, parts):
                total += len(part) + (3 if result else 0)
                result.append(part)
                if total > 1500:
                    break
            text = " - ".join(result)[:2000] or None
            if text:
                invoke_db(REDIS_COMMANDS.S_SET_INT, redis_key, -1, RAW_PATH_CONSTANTS.HREF_TIMEOUT)
            else:
                invoke_db(REDIS_COMMANDS.S_SET_INT, redis_key, is_crawled + 1, RAW_PATH_CONSTANTS.HREF_TIMEOUT)
            return text[:1000] if text else None
        except Exception as ex:
            return None

    @staticmethod
    def is_valid_url(url):
      archive_extensions = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}
      if not url:
        return False
      if helper_method.get_network_type(url) == "onion":
        return False
      path = urlparse(url).path
      ext = os.path.splitext(path)[1].lower()
      if ext in archive_extensions:
        return False
      return True

    @staticmethod
    def empty_screenshot_base64() -> str:
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+yv1cAAAAASUVORK5CYII="

    @staticmethod
    def get_screenshot_base64(page, search_string, base_url):
        empty_screenshot = helper_method.empty_screenshot_base64()
        try:
            storage_key = REDIS_KEYS.LEAK_PARSED + helper_method.get_host_name(base_url)
            url_previously_parsed = redis_controller().invoke_trigger(
                REDIS_COMMANDS.S_GET_BOOL, [storage_key, False, None]
            )
            if url_previously_parsed:
                return empty_screenshot

            try:
                if page.evaluate("document.readyState") != "complete":
                    page.wait_for_load_state("networkidle", timeout=4000)
            except Exception as ex:
                log.g().e(str(ex) + " : screenshot : " + base_url)

            if search_string:
                search_string = helper_method.remove_stopwords_from_string(search_string)
                search_string = re.sub(r"[^\w\s-]", "", search_string).strip()
                tokens = search_string.split()
                if tokens:
                    first_token = tokens[0]
                    element = page.locator(f":text('{first_token}')").first
                    element.wait_for(timeout=4000)
                    element.evaluate("el => el.scrollIntoView({ block: 'center', behavior: 'instant' })")

            screenshot_bytes = page.screenshot(timeout=4000)
            return base64.b64encode(screenshot_bytes).decode("utf-8")
        except Exception as ex:
            log.g().e(str(ex) + " : screenshot : " + base_url)
            return empty_screenshot

    @staticmethod
    def is_code(text: str, threshold: float = 0.5) -> bool:
        STOPWORDS = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will",
                     "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "no", "just", "him", "know", "take", "people", "into", "year",
                     "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
                     "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"}
        words = re.findall(r"[A-Za-z']+", text)
        n_words = len(words)
        stop = sum(1 for w in words if w.lower() in STOPWORDS)
        stop_ratio = (stop / n_words) if n_words else 0.0
        code_kw = re.findall(r"\b(def|class|import|return|if|else|elif|while|for|try|catch|finally|public|private|static|void|int|string|function|var|let|const|lambda|=>|switch|case)\b", text, re.IGNORECASE)
        sym = re.findall(r"[{}();=<>\[\]|&/*+\-:%^~`]", text)
        ops = re.findall(r"(==|===|!=|<=|>=|->|::|:=|=>|\\n\\t|\t)", text)
        snake = re.findall(r"\b[a-z]+_[a-z0-9_]+\b", text)
        camel = re.findall(r"\b[a-z]+[A-Z][A-Za-z0-9]*\b", text)
        lines = [ln for ln in text.splitlines() if ln.strip()]
        indented = sum(1 for ln in lines if re.match(r"^\s{2,}|\t", ln))
        code_score = 0
        code_score += 2 if len(sym) >= 2 else (1 if sym else 0)
        code_score += 2 if len(ops) else 0
        code_score += 2 if indented >= 1 and len(lines) >= 2 else 0
        code_score += 1 if len(code_kw) >= 2 else (0 if len(code_kw) == 1 else 0)
        code_score += 1 if len(snake) >= 1 else 0
        code_score += 1 if len(camel) >= 1 else 0
        text_score = 0
        text_score += 2 if stop_ratio >= 0.25 else (1 if stop_ratio >= 0.15 else 0)
        text_score += 1 if n_words >= 6 and not sym and not indented else 0
        return code_score > text_score

    @staticmethod
    def get_network_type(url: str):
        try:
            if not url.startswith("http"):
                url = HTTP_SCHEME + url
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return "invalid"
            if re.search(r"\.onion$", parsed_url.netloc, re.IGNORECASE):
                return "onion"
            if re.search(r"\.i2p$", parsed_url.netloc, re.IGNORECASE):
                return "i2p"
            return "clearnet"
        except Exception as ex:
            log.g().e(ex)
            return "invalid"

    @staticmethod
    def extract_text_from_html(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        return helper_method.clean_text(text)

    @staticmethod
    def clear_hosts_file(file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w'):
                pass

        except Exception as ex:
            log.g().e(ex)

    @staticmethod
    def get_host_name(p_url):
        m_parsed_uri = urlparse(p_url)
        m_netloc = m_parsed_uri.netloc

        if m_netloc.startswith('www.'):
            m_netloc = m_netloc[4:]

        netloc_parts = m_netloc.split('.')

        if len(netloc_parts) > 2:
            m_host_name = netloc_parts[-2]
        elif len(netloc_parts) == 2:
            m_host_name = netloc_parts[0]
        else:
            m_host_name = m_netloc

        return m_host_name

    @staticmethod
    def get_class_name(p_url):
        m_parsed_uri = urlparse(p_url)
        m_netloc = m_parsed_uri.netloc
        if m_netloc.startswith('www.'):
            m_netloc = m_netloc[4:]

        netloc_parts = m_netloc.split('.')
        if len(netloc_parts) > 1:
            m_host_name = '.'.join(netloc_parts[:-1])
        else:
            m_host_name = m_netloc
        return m_host_name

    @staticmethod
    def get_service_ip():
        try:
            service_name = os.getenv('SEARCH_SERVICE', 'orion-search-web')
            service_ip = socket.gethostbyname(service_name)
            return f"{HTTP_SCHEME}{service_ip}:8080"
        except socket.error as e:
            return f"Error resolving service IP: {e}"

    @staticmethod
    def extract_zip(from_path, to_path):
        os.makedirs(to_path, exist_ok=True)
        try:
            with zipfile.ZipFile(from_path, 'r') as zip_ref:
                zip_ref.extractall(to_path)
        except Exception as ex:
            log.g().e(f"Error occurred while extracting {from_path}: {ex}")

    @staticmethod
    def split_host_url(p_url):
        m_parsed_uri = urlparse(p_url)
        m_host_url = '{uri.scheme}://{uri.netloc}/'.format(uri=m_parsed_uri)
        if m_host_url.endswith("/"):
            m_host_url = m_host_url[:-1]

        m_subhost = p_url[len(m_host_url):]
        if len(m_subhost) == 1:
            m_subhost = "na"
        return m_host_url, m_subhost

    @staticmethod
    def normalize_slashes(p_url):
        p_url = str(p_url)
        segments = p_url.split('/')
        correct_segments = []
        for segment in segments:
            if segment != '':
                correct_segments.append(segment)
        normalized_url = '/'.join(correct_segments)
        normalized_url = normalized_url.replace("http:/", HTTP_SCHEME)
        normalized_url = normalized_url.replace("https:/", "https://")
        normalized_url = normalized_url.replace("ftp:/", "ftp://")
        return normalized_url

    @staticmethod
    def is_url_base_64(p_url):
        if str(p_url).startswith("duplicationHandlerService:"):
            return True
        else:
            return False

    @staticmethod
    def is_uri_validator(p_url):
        try:
            result = urlparse(p_url)
            return all([result.scheme, result.netloc])
        except Exception as ex:
            log.g().e(ex)
            return False

    @staticmethod
    def clear_folder(p_path):
        for f in os.listdir(p_path):
            try:
                os.remove(os.path.join(p_path, f))
            except Exception as ex:
                log.g().e(f"Error removing file {f}: {ex}")

    @staticmethod
    def write_content_to_path(p_path, p_content):
        m_url_path = p_path
        file = open(m_url_path, "wb")
        file.write(p_content)
        file.close()

    @staticmethod
    def get_host_url(p_url):
        m_parsed_uri = urlparse(p_url)
        m_host_url = '{uri.scheme}://{uri.netloc}/'.format(uri=m_parsed_uri)
        if m_host_url.endswith("/"):
            m_host_url = m_host_url[:-1]
        return m_host_url

    @staticmethod
    def hash_file_name(p_url):
        full_url = p_url.strip()
        md5_hash = hashlib.md5(full_url.encode('utf-8')).hexdigest()
        return ''.join(str(int(c, 16) % 10) for c in md5_hash)[:32]

    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
