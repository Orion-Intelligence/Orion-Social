import json

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import TwitchConstants

constants = TwitchConstants


def probe_url(username: str) -> str:
    return TwitchConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    payload = json.dumps({"query": TwitchConstants.GQL_QUERY.format(username=username)})
    headers = {"Client-Id": TwitchConstants.GQL_CLIENT_ID, "Content-Type": "application/json"}
    return http_client.post(TwitchConstants.GQL_URL, payload, headers)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or "data" not in payload:
        return VerdictConstants.UNKNOWN, {}
    user = (payload.get("data") or {}).get("user")
    if user is None:
        return VerdictConstants.ABSENT, {}
    if not isinstance(user, dict) or not user.get("id"):
        return VerdictConstants.UNKNOWN, {}
    followers = user.get("followers") or {}
    roles = user.get("roles") if isinstance(user.get("roles"), dict) else {}
    info = {
        "display_name": parse.clean(user.get("displayName")),
        "username": parse.text(user.get("login")),
        "description": parse.clean(user.get("description")),
        "avatar": parse.text(user.get("profileImageURL")),
        "cover": parse.text(user.get("bannerImageURL") or user.get("offlineImageURL")),
        "id": parse.text(user.get("id")),
        "created_at": parse.text(user.get("createdAt")),
        "followers": parse.text(followers.get("totalCount") if isinstance(followers, dict) else None),
        "partner": "true" if roles.get("isPartner") else "",
        "affiliate": "true" if roles.get("isAffiliate") else "",
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
    (r"(?P<id>[^/]+)(?:/.*)?", "profile"),
)

