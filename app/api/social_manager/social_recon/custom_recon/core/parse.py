import json
import re
from html import unescape
from typing import Any

from api.social_manager.social_recon.constants.custom_recon_constants import ParseConstants


def text(value: Any) -> str:
    return str(value) if value else ""


def title(body: str) -> str:
    match = ParseConstants.TITLE.search(body or "")
    return re.sub(r"\s+", " ", unescape(match.group(1))).strip() if match else ""


def meta(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for tag in ParseConstants.META.finditer(body or ""):
        raw = tag.group(0)
        key, value = ParseConstants.KEY.search(raw), ParseConstants.VALUE.search(raw)
        if key and value:
            out.setdefault(key.group(1).strip().lower(), unescape(value.group(1)).strip())
    return out


def as_json(body: str) -> Any:
    try:
        return json.loads(body or "")
    except Exception:
        return None


def _unescape_url(value: str) -> str:
    return (
        (value or "")
        .replace("\\u002F", "/")
        .replace("\\u002f", "/")
        .replace("\\/", "/")
        .replace("\\u0026", "&")
        .replace("&amp;", "&")
    )


def is_generic_image(url: str) -> bool:
    lowered = (url or "").casefold()
    return not lowered or any(marker in lowered for marker in ParseConstants.GENERIC_IMAGE)


def json_url(body: str, *keys: str) -> str:
    for key in keys:
        match = re.search(rf'"{re.escape(key)}"\s*:\s*"(https?:(?:[^"\\]|\\.){{10,400}}?)"', body or "")
        if match:
            candidate = _unescape_url(match.group(1))
            if not is_generic_image(candidate):
                return candidate
    return ""


def pattern_url(body: str, pattern: str) -> str:
    if not pattern:
        return ""
    match = re.search(pattern, body or "", re.DOTALL)
    if not match:
        return ""
    candidate = _unescape_url(match.group(1))
    return "" if is_generic_image(candidate) else candidate


def images(body: str, avatar_keys: tuple[str, ...] = (), cover_keys: tuple[str, ...] = (), avatar_pattern: str = "", cover_pattern: str = "") -> dict[str, str]:
    tags = meta(body)
    avatar = _unescape_url(tags.get("og:image") or tags.get("twitter:image") or "")
    if is_generic_image(avatar):
        avatar = ""
    if not avatar and avatar_keys:
        avatar = json_url(body, *avatar_keys)
    if not avatar:
        avatar = pattern_url(body, avatar_pattern)
    cover = json_url(body, *cover_keys) if cover_keys else ""
    if not cover:
        cover = pattern_url(body, cover_pattern)
    return {key: value for key, value in (("avatar", avatar), ("cover", cover)) if value}


def social_info(body: str, avatar_keys: tuple[str, ...] = (), cover_keys: tuple[str, ...] = (), avatar_pattern: str = "", cover_pattern: str = "") -> dict[str, str]:
    tags = meta(body)
    info = {
        "display_name": tags.get("og:title") or tags.get("twitter:title") or "",
        "description": tags.get("og:description") or tags.get("twitter:description") or "",
    }
    info.update(images(body, avatar_keys, cover_keys, avatar_pattern, cover_pattern))
    return {key: value for key, value in info.items() if value}


def counts(value: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for number, label in re.findall(r"([\d.,]+[KMB]?)\s+(Followers|Following|Threads|Posts|Friends)", value or "", re.IGNORECASE):
        out[label.lower()] = number
    return out
