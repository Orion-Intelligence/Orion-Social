import re
import urllib.parse

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import YouTubeConstants

constants = YouTubeConstants


def probe_url(username: str) -> str:
    return YouTubeConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, YouTubeConstants.AVATAR_KEYS, YouTubeConstants.COVER_KEYS, cover_pattern=YouTubeConstants.COVER_PATTERN)
    if info.get("description"):
        info["description"] = parse.clean(info["description"])
    handle = re.search(r'"canonicalBaseUrl":"/@([\w.-]+)"', body) or re.search(r'youtube\.com/@([\w.-]+)"', body)
    if handle:
        info["username"] = handle.group(1)
    subscribers = re.search(YouTubeConstants.SUBSCRIBERS, body)
    if subscribers:
        info["subscribers"] = parse.clean(subscribers.group(1)).replace(" subscribers", "")
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    oembed = YouTubeConstants.OEMBED.format(url=urllib.parse.quote(final_url or "", safe=""))
    code, payload, _ = http_client.fetch(oembed)
    if code == 404:
        return VerdictConstants.ABSENT, {}
    data = parse.as_json(payload) if code == 200 else None
    if isinstance(data, dict) and data.get("title"):
        info = {
            "title": parse.clean(data.get("title")),
            "author": parse.clean(data.get("author_name")),
            "author_url": parse.text(data.get("author_url")),
            "image": parse.text(data.get("thumbnail_url")),
        }
        return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    meta = parse.meta(body)
    image = parse.text(meta.get("og:image") or meta.get("twitter:image"))
    info = {
        "title": parse.clean(meta.get("og:title") or parse.title(body)),
        "description": parse.clean(meta.get("og:description") or meta.get("description")),
        "image": "" if parse.is_generic_image(image) else image,
    }
    entity = parse.ld_entity(body, "Article", "VideoObject", "DiscussionForumPosting", "Question", "SocialMediaPosting", "CreativeWork", "MusicRecording", "Product")
    if entity:
        if not info["description"]:
            info["description"] = parse.clean(entity.get("description") or entity.get("headline"))
        author = entity.get("author")
        if isinstance(author, list) and author:
            author = author[0]
        if isinstance(author, dict):
            info["author"] = parse.clean(author.get("name"))
        elif isinstance(author, str):
            info["author"] = parse.clean(author)
        info["published"] = parse.text(entity.get("datePublished") or entity.get("uploadDate"))
    if not any(info.get(key) for key in ("title", "description", "image")):
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

HOSTS = ("youtu.be",)
ROUTES = (
    (r"@(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"channel/(?P<id>UC[\w-]+)(?:/.*)?", "channel"),
)

