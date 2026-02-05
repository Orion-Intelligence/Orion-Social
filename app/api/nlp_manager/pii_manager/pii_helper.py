# pii_helper.py
import re
from urllib.parse import urlparse
from phonenumbers import parse, is_valid_number, geocoder, carrier

_URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
_CODE_FENCE_RE = re.compile(r"```.*?```", re.S)
_FILENAME_RE = re.compile(r"\b[\w.-]+\.(?:exe|dll|sys|msi|scr|bat|zip|rar|7z|tar|gz|xz|bz2|tgz|tbz2|zst|apk|aab|ipa|iso|img|vhd|vhdx|ova|ovf|ps1|vbs|js|jse|jar|class|war|so|dylib|o|a|pdf|doc|docx|xls|xlsx|ppt|pptx|csv|rtf|txt|log)\b", re.I)
_HASH_LABEL_RE = re.compile(r"^\s*(?:md5|sha1|sha256|sha512|icon\s*hash)\s*:\s*", re.I | re.M)
_FILE_EXT_RE = re.compile(r".*\.(exe|dll|sys|msi|scr|bat|zip|rar|7z|tar|gz|xz|bz2|tgz|tbz2|zst|apk|aab|ipa|iso|img|vhd|vhdx|ova|ovf|ps1|vbs|js|jse|jar|class|war|so|dylib|o|a|pdf|doc|docx|xls|xlsx|ppt|pptx|csv|rtf|txt|log)$", re.I)

def _span_in_any(text: str, start: int, end: int, patterns):
    for rx in patterns:
        for m in rx.finditer(text):
            if start >= m.start() and end <= m.end():
                return True
    return False

def _looks_like_bad_context(text: str, start: int, end: int):
    if _span_in_any(text, start, end, (_URL_RE, _CODE_FENCE_RE)):
        return True
    for m in _FILENAME_RE.finditer(text):
        if start >= m.start() and end <= m.end():
            return True
    line_start = text.rfind("\n", 0, start) + 1
    line = text[line_start:text.find("\n", line_start) if text.find("\n", line_start) != -1 else len(text)]
    if _HASH_LABEL_RE.match(line):
        return True
    return False

def _valid_ssn(digits: str):
    if len(digits) != 9 or not digits.isdigit():
        return False
    area, group, serial = digits[:3], digits[3:5], digits[5:]
    if area in {"000", "666"} or area.startswith("9"):
        return False
    if group == "00" or serial == "0000":
        return False
    return True

def _aba_routing_ok(digits: str):
    if len(digits) != 9 or not digits.isdigit():
        return False
    weights = [3, 7, 1] * 3
    s = sum(int(d) * w for d, w in zip(digits, weights))
    return s % 10 == 0

def _plausible_acct(digits: str):
    if not digits.isdigit() or len(digits) < 10 or len(digits) > 12:
        return False
    if len(set(digits)) == 1:
        return False
    if digits in ("0123456789", "9876543210"):
        return False
    return True

def _strip_punct(s: str):
    trims = ".,:;\"'“”‘’()[]{}<>"
    start = 0
    end = len(s)
    while start < end and s[start] in trims:
        start += 1
    while end > start and s[end - 1] in trims:
        end -= 1
    return s[start:end]

def _split_kv(token: str):
    for sep in ['=', ':']:
        if sep in token:
            k, v = token.split(sep, 1)
            return k, v
    return token, ""

def _is_username(token: str):
    if not (3 <= len(token) <= 30):
        return False
    for c in token:
        if not (c.isalnum() or c in "._-"):
            return False
    return True

def _is_password(token: str):
    if not (6 <= len(token) <= 40):
        return False
    bad = set(' \t"\'<>,;')
    return all(c not in bad for c in token)

def _digits_count(s: str):
    return sum(1 for ch in s if ch.isdigit())

def _normalize_domain(v: str):
    s = v.strip()
    if "://" in s:
        parsed = urlparse(s)
        host = parsed.netloc
    else:
        host = s
    if host.startswith("www."):
        host = host[4:]
    return host

def _extract_ip_from_url(u: str):
    try:
        host = urlparse(u).hostname
        if not host:
            return None
        import ipaddress
        ipaddress.ip_address(host)
        return host
    except Exception:
        return None

_B58_ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_B58_IDX = {c: i for i, c in enumerate(_B58_ALPH)}

def _is_base58(s: str):
    return all(ch in _B58_IDX for ch in s)

def clean_text(text: str):
    s = text.encode('utf-8', 'ignore').decode('unicode_escape', 'ignore')
    s = s.replace('\r', '. ').replace('\n', '. ').replace('\t', '. ').replace('\\', '. ')
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.strip()

def deduplicate_key(key: str):
    dedup_map = {
        'm_ipv4_addresses': 'm_ip', 'm_ipv6_addresses': 'm_ip', 'm_ipv4_cidrs': 'm_ip',
        'm_cves': 'm_cve',
        'm_phone_numbers': 'm_phone_number', 'm_telephone_nums': 'm_phone_number',
        'm_domains': 'm_domain',
        'm_weblink': 'm_url', 'm_websites': 'm_url',
        'm_urls': 'm_url', 'm_unencoded_urls': 'm_url'
    }
    return dedup_map.get(key, key)

def validate_international_phone(number: str):
    if not number.startswith("+"):
        return False, None, None
    try:
        parsed = parse(number, None)
        if not is_valid_number(parsed):
            return False, None, None
        country = geocoder.description_for_number(parsed, "en")
        provider = carrier.name_for_number(parsed, "en")
        return True, country, provider
    except Exception:
        return False, None, None
