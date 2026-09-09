import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import KitsuConstants

constants = KitsuConstants


def probe_url(username: str) -> str:
    return KitsuConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and isinstance(payload.get("data"), list) and not payload["data"]:
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and isinstance(payload.get("data"), list) and payload["data"] and isinstance(payload["data"][0], dict)):
        return VerdictConstants.UNKNOWN, {}
    attributes = payload["data"][0].get("attributes") if isinstance(payload["data"][0].get("attributes"), dict) else {}
    avatar = attributes.get("avatar") if isinstance(attributes.get("avatar"), dict) else {}
    cover = attributes.get("coverImage") if isinstance(attributes.get("coverImage"), dict) else {}
    info = {
        "display_name": parse.clean(attributes.get("name")),
        "username": parse.text(attributes.get("slug")),
        "description": parse.clean(attributes.get("about")),
        "avatar": parse.text(avatar.get("original")),
        "cover": parse.text(cover.get("original")),
        "id": parse.text(payload["data"][0].get("id")),
        "location": parse.clean(attributes.get("location")),
        "followers": parse.text(attributes.get("followersCount")) if attributes.get("followersCount") else "",
        "following": parse.text(attributes.get("followingCount")) if attributes.get("followingCount") else "",
        "gender": parse.clean(attributes.get("gender")),
        "created_at": parse.text(attributes.get("createdAt")),
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

HOSTS = ("kitsu.app",)
ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)

