import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GameJoltConstants

constants = GameJoltConstants


def probe_url(username: str) -> str:
    return GameJoltConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or "payload" not in payload:
        return VerdictConstants.UNKNOWN, {}
    user = (payload.get("payload") or {}).get("user") if isinstance(payload.get("payload"), dict) else None
    if not isinstance(user, dict) or not user.get("username"):
        return VerdictConstants.ABSENT, {}
    avatar_item = user.get("avatar_media_item") if isinstance(user.get("avatar_media_item"), dict) else {}
    header_item = user.get("header_media_item") if isinstance(user.get("header_media_item"), dict) else {}
    info = {
        "display_name": parse.clean(user.get("display_name") or user.get("name")),
        "username": parse.text(user.get("username")),
        "avatar": parse.text(avatar_item.get("img_url") or user.get("img_avatar")),
        "cover": parse.text(header_item.get("img_url")),
        "id": parse.text(user.get("id")),
        "followers": parse.text(user.get("follower_count")) if user.get("follower_count") else "",
        "following": parse.text(user.get("following_count")) if user.get("following_count") else "",
        "likes": parse.text(user.get("like_count")) if user.get("like_count") else "",
        "website": parse.text(user.get("web_site")),
        "created_at": parse.text(user.get("created_on")),
        "verified": "true" if user.get("is_verified") else "",
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
    ("@(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("c/(?P<id>[^/]+)(?:/.*)?", "group"),
)

