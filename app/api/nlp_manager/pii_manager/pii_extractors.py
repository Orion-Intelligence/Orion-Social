import validators
import pycountry
from nltk import TweetTokenizer
from phonenumbers import PhoneNumberMatcher, geocoder
from twitter_text import Extractor
from weakref import WeakKeyDictionary
import re
from collections import defaultdict

from api.nlp_manager.pii_manager.ioc_parser import _IOCParser
from crawler.crawler_services.log_manager.log_controller import log
from api.nlp_manager.pii_manager.pii_helper import (
    _strip_punct,
    _split_kv,
    _is_username,
    _is_password,
    validate_international_phone,
    _looks_like_bad_context
)

_SUPPORTED_ENTITIES_CACHE = WeakKeyDictionary()
_ORG_RE = re.compile(r"[A-Za-z]{5,14}\Z")
_USERNAME_RE = re.compile(r"[A-Za-z][A-Za-z0-9._-]{2,19}\Z")

def extract_hashtags_mentions(text: str):
    ex = Extractor(text)
    tags = {"#" + t.lower() for t in ex.extract_hashtags()}
    mentions = {"@" + u.lower() for u in ex.extract_mentioned_screen_names()}
    return tags, mentions

def extract_credentials(text: str):
    tokens = [_strip_punct(t) for t in TweetTokenizer().tokenize(text)]
    user_labels = {"username", "user", "login", "usr"}
    pass_labels = {"password", "pass", "pwd"}
    pairs = []
    last_user = None
    i = 0
    while i < len(tokens):
        tk = tokens[i]
        key, val = _split_kv(tk)
        lkey = key.lower()
        if lkey in user_labels:
            cand = val if val else (tokens[i + 1] if i + 1 < len(tokens) else "")
            cand = _strip_punct(cand)
            if _is_username(cand):
                last_user = cand
        elif lkey in pass_labels:
            cand = val if val else (tokens[i + 1] if i + 1 < len(tokens) else "")
            cand = _strip_punct(cand)
            if _is_password(cand) and last_user:
                pairs.append((last_user, cand))
                last_user = None
        i += 1
    email_usernames = set()
    for tk in tokens:
        if '@' in tk and validators.email(tk):
            local = tk.split('@', 1)[0]
            if _is_username(local):
                email_usernames.add(local)
    return pairs + [(u, "") for u in email_usernames]


def extract_iocs_from_text(text):
    _PARSER = _IOCParser()
    return _PARSER.parse(text)

def extract_phone_data(text: str, exclude_set):
    detected, countries = set(), set()
    try:
        for match in PhoneNumberMatcher(text, None):
            raw = match.raw_string.strip()
            if not raw.startswith('+'):
                continue
            if raw in exclude_set:
                continue
            ok, _, _ = validate_international_phone(raw)
            if not ok:
                continue
            detected.add(raw)
            cn = geocoder.country_name_for_number(match.number, "en")
            if cn:
                countries.add(cn)
    except Exception as ex:
        log.g().i(ex)
    return detected, countries


def extract_countries_from_text(text: str):
    resolved = set()
    seen = {}
    tokens = re.findall(r"\w+", text)
    max_len = 3
    for i in range(len(tokens)):
        for j in range(i + 1, min(i + max_len, len(tokens)) + 1):
            cand = " ".join(tokens[i:j])
            if cand in seen:
                if seen[cand]:
                    resolved.add(seen[cand])
                continue
            try:
                c = pycountry.countries.lookup(cand)
                if (j - i) == 1:
                    tok = tokens[i]
                    if not (tok[:1].isupper() and tok[1:].islower()):
                        seen[cand] = None
                        continue
                if cand.lower() in {c.name.lower(), getattr(c, "official_name", "").lower()}:
                    resolved.add(c.name)
                    seen[cand] = c.name
                else:
                    seen[cand] = None
            except LookupError:
                seen[cand] = None
    return resolved


# noinspection PyTypeChecker
def extract_currencies(text: str):
    sym_to_code = {"$":"USD","€":"EUR","£":"GBP","¥":"JPY","₹":"INR","₨":"PKR","₩":"KRW","₱":"PHP","₪":"ILS","₫":"VND","₭":"LAK","₮":"MNT","₦":"NGN","₲":"PYG","₵":"GHS","₸":"KZT","₴":"UAH","₽":"RUB"}
    sym_class = "[" + re.escape("".join(sym_to_code.keys())) + "]"
    codes = {c.alpha_3.upper() for c in pycountry.currencies if getattr(c, "alpha_3", None)}
    names = {c.name.lower(): c.alpha_3.upper() for c in pycountry.currencies if getattr(c, "name", None) and getattr(c, "alpha_3", None)}
    out = set()
    for m in re.finditer(r'(?i)(?<!\w)\d+(?:\.\d+)?\s*([A-Za-z]{3})(?!\w)', text):
        code = m.group(1).upper()
        if code in codes:
            out.add(code)
    if names:
        name_re = re.compile(r'(?i)(?<!\w)\d+(?:\.\d+)?\s*(' + "|".join(re.escape(n) for n in sorted(names.keys(), key=len, reverse=True)) + r')\b')
        for m in name_re.finditer(text):
            out.add(names[m.group(1).lower()])
    for m in re.finditer(rf'(?i)(?<!\w)({sym_class})\s*\d+(?:\.\d+)?', text):
        out.add(sym_to_code[m.group(1)])
    return sorted(out)

def extract_social_profiles(text: str):
    platforms = {
        "twitter": r"(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)\/[A-Za-z0-9_]{1,15}",
        "facebook": r"(?:https?:\/\/)?(?:www\.)?facebook\.com\/[A-Za-z0-9\.]+",
        "instagram": r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/[A-Za-z0-9_.]+",
        "linkedin": r"(?:https?:\/\/)?(?:[\w]+\.)?linkedin\.com\/in\/[A-Za-z0-9\-_]+",
        "github": r"(?:https?:\/\/)?(?:www\.)?github\.com\/[A-Za-z0-9\-_]+",
        "youtube": r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:c|channel|user)\/[A-Za-z0-9\-_]+",
        "tiktok": r"(?:https?:\/\/)?(?:www\.)?tiktok\.com\/@[\w.]+",
        "pinterest": r"(?:https?:\/\/)?(?:www\.)?pinterest\.com\/[A-Za-z0-9\-_\/]+",
        "reddit": r"(?:https?:\/\/)?(?:www\.)?reddit\.com\/user\/[A-Za-z0-9\-_]+",
        "telegram": r"(?:https?:\/\/)?t\.me\/[A-Za-z0-9_]+",
        "generic": r"(?:https?:\/\/)?[A-Za-z0-9\.\-]+\/@[\w.]+",
        "snapchat": r"(?:https?:\/\/)?(?:www\.)?snapchat\.com\/add\/[A-Za-z0-9\-_]+",
        "vk": r"(?:https?:\/\/)?(?:www\.)?vk\.com\/[A-Za-z0-9\-_]+",
        "weibo": r"(?:https?:\/\/)?(?:www\.)?weibo\.com\/[A-Za-z0-9\-_]+",
        "threads": r"(?:https?:\/\/)?(?:www\.)?threads\.net\/@[\w.]+",
        "bluesky": r"(?:https?:\/\/)?bsky\.app\/profile\/[A-Za-z0-9\.\-]+",
        "medium": r"(?:https?:\/\/)?(?:www\.)?medium\.com\/@[A-Za-z0-9\-_]+",
        "twitch": r"(?:https?:\/\/)?(?:www\.)?twitch\.tv\/[A-Za-z0-9_]+"
    }

    results = []
    platforms_found = set()

    for name, pattern in platforms.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            if not m.lower().startswith("http"):
                m = "https://" + m.lstrip("/")
            results.append(m)
            platforms_found.add(name)

    return list(set(results)), list(platforms_found)

def extract_spacy_entities(spacy_nlp, text: str, excluded_labels):
    return {(ent.text, ent.label_) for ent in spacy_nlp(text).ents if ent.label_ not in excluded_labels}

def extract_mitre_techniques(text: str, mitre_techniques, threshold=70, scorer=None):
    if scorer is None:
        from rapidfuzz.fuzz import token_set_ratio as scorer
    matched_names, matched_types = set(), set()
    sentences = [s.strip().lower() for s in re.split(r"[.!?;\n\r]+", text) if s.strip()]
    for s in sentences:
        for t in mitre_techniques:
            score = scorer(s, t["keywords"])
            if score >= threshold:
                matched_names.add(t["name"])
                matched_types.add(t["type"])
    return sorted(matched_names), sorted(matched_types)

def extract_presidio_entities(analyzer, text: str, already_found):
    text = text[:2000]
    if not text:
        return {}
    if not isinstance(already_found, set):
        already_found = set(already_found)

    presidio_entities = defaultdict(set)
    excluded = {"US_SSN", "DATE_TIME", "URL", "CRYPTO", "IP_ADDRESS", "PRODUCT", "CARDINAL"}
    label_map = {
        "US_SSN_STRICT": "US_SSN",
        "US_PASSPORT_CTX": "US_PASSPORT",
        "US_BANK_ROUTING_VALID": "US_BANK_ROUTING",
        "US_BANK_ACCOUNT_CTX": "US_BANK_ACCOUNT",
    }
    requested = [
        'AU_ABN','US_PASSPORT','UK_NINO','AU_ACN','US_BANK_ACCOUNT_CTX','SG_NRIC_FIN',
        'US_SSN_STRICT','AU_MEDICARE','ORGANIZATION','US_DRIVER_LICENSE','NRP',
        'US_BANK_NUMBER','PERSON','AU_TFN','MEDICAL_LICENSE','CREDIT_CARD',
        'US_ITIN','US_BANK_ROUTING_VALID','UK_NHS','LOCATION','IBAN_CODE'
    ]

    supported = _SUPPORTED_ENTITIES_CACHE.get(analyzer)
    if supported is None:
        supported = set(analyzer.get_supported_entities(language="en"))
        _SUPPORTED_ENTITIES_CACHE[analyzer] = supported
    entities_arg = [e for e in requested if e in supported] or None

    for r in analyzer.analyze(text=text, language="en", score_threshold=0.3, entities=entities_arg):
        if r.entity_type in excluded:
            continue
        if _looks_like_bad_context(text, r.start, r.end):
            continue
        value = text[r.start:r.end]
        if value in already_found:
            continue
        normalized_label = label_map.get(r.entity_type, r.entity_type)
        if normalized_label == "ORGANIZATION":
            if not _ORG_RE.fullmatch(value):
                continue
        if normalized_label == "USERNAME":
            if not _USERNAME_RE.fullmatch(value):
                continue
        presidio_entities[normalized_label].add(value)

    return {label: sorted(values) for label, values in presidio_entities.items()}
