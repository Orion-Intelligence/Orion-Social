import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BlueskyConstants

constants = BlueskyConstants


def handle(username: str) -> str:
    return username if "." in username else username + BlueskyConstants.DEFAULT_DOMAIN


def probe_url(username: str) -> str:
    return BlueskyConstants.API_URL.format(handle=handle(username))


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 400:
        payload = parse.as_json(body)
        message = parse.text((payload or {}).get("message")).casefold() if isinstance(payload, dict) else ""
        return (VerdictConstants.ABSENT, {}) if "not found" in message else (VerdictConstants.UNKNOWN, {})
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or not payload.get("did"):
        return VerdictConstants.UNKNOWN, {}
    associated = payload.get("associated") if isinstance(payload.get("associated"), dict) else {}
    verification = payload.get("verification") if isinstance(payload.get("verification"), dict) else {}
    info = {
        "display_name": parse.clean(payload.get("displayName")),
        "username": parse.text(payload.get("handle")),
        "description": parse.clean(payload.get("description")),
        "avatar": parse.text(payload.get("avatar")),
        "cover": parse.text(payload.get("banner")),
        "id": parse.text(payload.get("did")),
        "followers": parse.text(payload.get("followersCount")),
        "following": parse.text(payload.get("followsCount")),
        "posts": parse.text(payload.get("postsCount")),
        "created_at": parse.text(payload.get("createdAt")),
        "lists": parse.text(associated.get("lists")) if associated.get("lists") else "",
        "feeds": parse.text(associated.get("feedgens")) if associated.get("feedgens") else "",
        "starter_packs": parse.text(associated.get("starterPacks")) if associated.get("starterPacks") else "",
        "verified": "true" if verification.get("verifiedStatus") == "valid" else "",
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
    (r"profile/(?P<id>[^/]+)", "profile"),
)

