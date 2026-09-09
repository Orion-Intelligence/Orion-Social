import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import DailymotionConstants

constants = DailymotionConstants


def probe_url(username: str) -> str:
    return DailymotionConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and isinstance(payload.get("error"), dict) and payload["error"].get("code") == 404:
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and payload.get("id")):
        return VerdictConstants.UNKNOWN, {}
    avatar = parse.text(payload.get("avatar_720_url"))
    info = {
        "display_name": parse.clean(payload.get("screenname")),
        "username": parse.text(payload.get("username")),
        "description": parse.clean(payload.get("description")),
        "avatar": "" if DailymotionConstants.DEFAULT_AVATAR in avatar else avatar,
        "cover": parse.text(payload.get("cover_url")),
        "id": parse.text(payload.get("id")),
        "followers": parse.text(payload.get("followers_total")) if payload.get("followers_total") else "",
        "videos": parse.text(payload.get("videos_total")) if payload.get("videos_total") else "",
        "views": parse.text(payload.get("views_total")) if payload.get("views_total") else "",
        "created_at": parse.text(payload.get("created_time")),
        "country": parse.text(payload.get("country")),
        "language": parse.text(payload.get("language")),
        "verified": "true" if payload.get("verified") else "",
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
    ("(?P<id>[^/]+)", "profile"),
)

