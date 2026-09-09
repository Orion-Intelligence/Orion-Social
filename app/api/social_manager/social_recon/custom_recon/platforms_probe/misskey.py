import json

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import MisskeyConstants

constants = MisskeyConstants


def probe_url(username: str) -> str:
    return MisskeyConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    payload = json.dumps({"username": username})
    return http_client.post(MisskeyConstants.API_URL, payload, {"Content-Type": "application/json"})


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and payload.get("error"):
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(payload.get("name") or payload.get("username")),
        "username": parse.text(payload.get("username")),
        "description": parse.clean(payload.get("description")),
        "avatar": parse.text(payload.get("avatarUrl")),
        "cover": parse.text(payload.get("bannerUrl")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text(payload.get("createdAt")),
        "location": parse.clean(payload.get("location")),
        "followers": parse.text(payload.get("followersCount")) if payload.get("followersCount") else "",
        "following": parse.text(payload.get("followingCount")) if payload.get("followingCount") else "",
        "posts": parse.text(payload.get("notesCount")) if payload.get("notesCount") else "",
        "bot": "true" if payload.get("isBot") else "",
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
    ("@(?P<id>[^/@]+)(?:/.*)?", "profile"),
)

