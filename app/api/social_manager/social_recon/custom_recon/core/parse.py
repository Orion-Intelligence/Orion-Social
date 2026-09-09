import json
import re
from html import unescape
from typing import Any

from api.social_manager.social_recon.constants.custom_recon_constants import ParseConstants


def text(value: Any) -> str:
    return str(value) if value else ""


def clean(value: Any) -> str:
    raw = unescape(unescape(str(value) if value else ""))
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw)).strip()


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


def json_ld(body: str) -> list[dict]:
    out: list[dict] = []
    for match in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', body or "", re.DOTALL | re.IGNORECASE):
        parsed = as_json(match.group(1).strip())
        for item in parsed if isinstance(parsed, list) else [parsed]:
            if isinstance(item, dict):
                out.append(item)
                graph = item.get("@graph")
                if isinstance(graph, list):
                    out.extend(node for node in graph if isinstance(node, dict))
    return out


def ld_entity(body: str, *types: str) -> dict:
    wanted = {value.casefold() for value in types}
    for node in json_ld(body):
        node_type = node.get("@type")
        labels = {str(node_type).casefold()} if isinstance(node_type, str) else {str(value).casefold() for value in node_type or []}
        if labels & wanted:
            return node
        entity = node.get("mainEntity")
        if isinstance(entity, dict):
            entity_type = entity.get("@type")
            entity_labels = {str(entity_type).casefold()} if isinstance(entity_type, str) else {str(value).casefold() for value in entity_type or []}
            if entity_labels & wanted:
                return entity
    return {}


def embedded_object(body: str, key: str) -> dict:
    start = (body or "").find(f'"{key}"')
    if start == -1:
        return {}
    opening = body.find("{", start)
    if opening == -1:
        return {}
    depth, in_string, escaped = 0, False, False
    for index in range(opening, len(body)):
        char = body[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                parsed = as_json(body[opening : index + 1])
                return parsed if isinstance(parsed, dict) else {}
    return {}


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


SOCIAL_DOMAINS = {
    "twitter.com": "twitter", "x.com": "twitter", "instagram.com": "instagram",
    "facebook.com": "facebook", "fb.com": "facebook", "youtube.com": "youtube",
    "youtu.be": "youtube", "tiktok.com": "tiktok", "linkedin.com": "linkedin",
    "github.com": "github", "gitlab.com": "gitlab", "twitch.tv": "twitch",
    "soundcloud.com": "soundcloud", "spotify.com": "spotify", "t.me": "telegram",
    "telegram.me": "telegram", "pinterest.com": "pinterest", "tumblr.com": "tumblr",
    "snapchat.com": "snapchat", "vk.com": "vk", "reddit.com": "reddit",
    "threads.net": "threads", "discord.gg": "discord", "discord.com": "discord",
    "patreon.com": "patreon", "bandcamp.com": "bandcamp", "medium.com": "medium",
    "behance.net": "behance", "dribbble.com": "dribbble", "vimeo.com": "vimeo",
    "flickr.com": "flickr", "deviantart.com": "deviantart",
}


def hrefs(value: Any) -> list[str]:
    return re.findall(r'href=["\']?(https?://[^"\'\s>]+)', str(value) if value else "")


def social_links(urls: Any) -> dict[str, str]:
    out: dict[str, str] = {}
    for url in urls if isinstance(urls, (list, tuple)) else []:
        value = _unescape_url(str(url or "")).strip()
        match = re.match(r"https?://([^/]+)", value, re.IGNORECASE)
        if not match:
            continue
        host = match.group(1).split("@")[-1].split(":")[0].casefold()
        host = host[4:] if host.startswith("www.") else host
        for domain, name in SOCIAL_DOMAINS.items():
            if (host == domain or host.endswith(f".{domain}")) and name not in out:
                out[name] = value
                break
    return out


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


def search_result(body: str) -> dict[str, str]:
    payload = as_json(body)
    matches = payload.get("matches") if isinstance(payload, dict) else None
    if not matches or not isinstance(matches[0], dict):
        return {}
    first = matches[0]
    info = {
        "display_name": clean(first.get("title")),
        "description": clean(first.get("body")),
        "avatar": text(first.get("image")),
    }
    return {key: value for key, value in info.items() if value}


def counts(value: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for number, label in re.findall(r"([\d.,]+[KMB]?)\s+(Followers|Following|Threads|Posts|Friends)", value or "", re.IGNORECASE):
        out[label.lower()] = number
    return out
