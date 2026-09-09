import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import WikipediaConstants

constants = WikipediaConstants


def probe_url(username: str) -> str:
    return WikipediaConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    users = ((payload.get("query") or {}).get("users")) if isinstance(payload, dict) else None
    if isinstance(users, list) and users and ("missing" in users[0] or "invalid" in users[0]):
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and isinstance(((payload.get("query") or {}).get("users")), list) and payload["query"]["users"] and payload["query"]["users"][0].get("userid")):
        return VerdictConstants.UNKNOWN, {}
    user = payload["query"]["users"][0]
    groups = [group for group in (user.get("groups") or []) if group not in ("*", "user", "autoconfirmed", "extendedconfirmed")]
    info = {
        "display_name": parse.text(user.get("name")),
        "username": parse.text(user.get("name")),
        "id": parse.text(user.get("userid")),
        "created_at": parse.text(user.get("registration")),
        "edits": parse.text(user.get("editcount")) if user.get("editcount") else "",
        "groups": ", ".join(groups),
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
    ("wiki/User:(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("wiki/(?P<id>[^/]+)", "page"),
)
