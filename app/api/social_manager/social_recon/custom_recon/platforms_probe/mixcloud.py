import re

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import MixcloudConstants

constants = MixcloudConstants


def probe_url(username: str) -> str:
    return MixcloudConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    pictures = payload.get("pictures") if isinstance(payload.get("pictures"), dict) else {}
    location = ", ".join(part for part in (parse.clean(payload.get("city")), parse.clean(payload.get("country"))) if part)
    info = {
        "display_name": parse.clean(payload.get("name")),
        "username": parse.text(payload.get("username")),
        "description": parse.clean(payload.get("biog")),
        "avatar": parse.text(pictures.get("extra_large") or pictures.get("large")),
        "location": location,
        "followers": parse.text(payload.get("follower_count")) if payload.get("follower_count") else "",
        "following": parse.text(payload.get("following_count")) if payload.get("following_count") else "",
        "tracks": parse.text(payload.get("cloudcast_count")) if payload.get("cloudcast_count") else "",
        "created_at": parse.text(payload.get("created_time")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    match = re.search(MixcloudConstants.CLOUDCAST_RE, final_url or "")
    if match:
        code, payload, _ = http_client.fetch(MixcloudConstants.CLOUDCAST_API.format(path=match.group(1)))
        if code == 404:
            return VerdictConstants.ABSENT, {}
        data = parse.as_json(payload) if code == 200 else None
        if isinstance(data, dict) and data.get("name"):
            info = {
                "title": parse.clean(data.get("name")),
                "author": parse.clean((data.get("user") or {}).get("name")),
                "plays": parse.text(data.get("play_count")) if data.get("play_count") else "",
                "likes": parse.text(data.get("favorite_count")) if data.get("favorite_count") else "",
                "duration": parse.text(data.get("audio_length")) if data.get("audio_length") else "",
                "created_at": parse.text(data.get("created_time")),
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

ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)

