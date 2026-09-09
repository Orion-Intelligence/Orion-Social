import json

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import RobloxConstants

constants = RobloxConstants


def probe_url(username: str) -> str:
    return RobloxConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    payload = json.dumps({"usernames": [username], "excludeBannedUsers": False})
    status, body, url = http_client.post(RobloxConstants.RESOLVE_URL, payload, {"Content-Type": "application/json"})
    if status != 200:
        return status, body, url
    data = (parse.as_json(body) or {}).get("data") if isinstance(parse.as_json(body), dict) else None
    if not data:
        return 200, json.dumps({"_absent": True}), url
    user_id = data[0].get("id")
    detail_status, detail_body, detail_url = http_client.fetch(RobloxConstants.DETAIL_URL.format(id=user_id))
    detail = parse.as_json(detail_body) if detail_status == 200 else None
    if not isinstance(detail, dict):
        return detail_status, detail_body, detail_url
    _, avatar_body, _ = http_client.fetch(RobloxConstants.AVATAR_URL.format(id=user_id))
    avatar = parse.as_json(avatar_body)
    if isinstance(avatar, dict) and isinstance(avatar.get("data"), list) and avatar["data"]:
        detail["_avatar"] = avatar["data"][0].get("imageUrl")
    return 200, json.dumps(detail), detail_url


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and payload.get("_absent"):
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and payload.get("id")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(payload.get("displayName") or payload.get("name")),
        "username": parse.text(payload.get("name")),
        "description": parse.clean(payload.get("description")),
        "avatar": parse.text(payload.get("_avatar")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text(payload.get("created")),
        "verified": "true" if payload.get("hasVerifiedBadge") else "",
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
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
    (r"users/(?P<id>\d+)(?:/.*)?", "profile"),
    (r"users/profile\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
    (r"(?:groups|communities)/(?P<id>\d+)(?:/.*)?", "group"),
)

