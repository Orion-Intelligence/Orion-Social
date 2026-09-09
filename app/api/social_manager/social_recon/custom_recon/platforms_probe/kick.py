import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import KickConstants

constants = KickConstants


def probe_url(username: str) -> str:
    return KickConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or not payload.get("id"):
        return VerdictConstants.UNKNOWN, {}
    user = payload.get("user") if isinstance(payload.get("user"), dict) else {}
    banner = payload.get("banner_image") if isinstance(payload.get("banner_image"), dict) else {}
    info = {
        "display_name": parse.clean(user.get("username")),
        "username": parse.text(payload.get("slug") or user.get("username")),
        "description": parse.clean(user.get("bio")),
        "avatar": parse.text(user.get("profile_pic")),
        "cover": parse.text(banner.get("url")),
        "id": parse.text(payload.get("id")),
        "followers": parse.text(payload.get("followers_count")) if payload.get("followers_count") else "",
        "verified": "true" if payload.get("verified") else "",
    }
    for key in ("instagram", "twitter", "youtube", "discord", "tiktok", "facebook"):
        value = parse.text(user.get(key))
        if value:
            info[key] = value
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
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)

