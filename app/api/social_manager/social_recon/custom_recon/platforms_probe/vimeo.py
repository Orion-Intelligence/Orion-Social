import re

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import VimeoConstants

constants = VimeoConstants


def probe_url(username: str) -> str:
    return VimeoConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("id")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(payload.get("display_name")),
        "username": parse.text(payload.get("profile_url")).rstrip("/").split("/")[-1] or parse.text(_final_url).rstrip("/").split("/")[-1],
        "description": parse.clean(payload.get("bio")),
        "avatar": parse.text(payload.get("portrait_huge") or payload.get("portrait_large")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text(payload.get("created_on")),
        "location": parse.clean(payload.get("location")),
        "website": parse.text(payload.get("url")),
        "videos": parse.text(payload.get("total_videos_uploaded")) if payload.get("total_videos_uploaded") else "",
        "pro": "true" if payload.get("is_pro") == "1" or payload.get("is_plus") == "1" else "",
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    match = re.search(VimeoConstants.VIDEO_RE, final_url or "")
    if match:
        code, payload, _ = http_client.fetch(VimeoConstants.VIDEO_API.format(id=match.group(1)))
        data = parse.as_json(payload) if code == 200 else None
        video = data[0] if isinstance(data, list) and data and isinstance(data[0], dict) else None
        if code == 404:
            return VerdictConstants.ABSENT, {}
        if video and video.get("title"):
            info = {
                "title": parse.clean(video.get("title")),
                "description": parse.clean(video.get("description")),
                "author": parse.clean(video.get("user_name")),
                "image": parse.text(video.get("thumbnail_large")),
                "plays": parse.text(video.get("stats_number_of_plays")) if video.get("stats_number_of_plays") else "",
                "likes": parse.text(video.get("stats_number_of_likes")) if video.get("stats_number_of_likes") else "",
                "duration": parse.text(video.get("duration")) if video.get("duration") else "",
                "created_at": parse.text(video.get("upload_date")),
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

