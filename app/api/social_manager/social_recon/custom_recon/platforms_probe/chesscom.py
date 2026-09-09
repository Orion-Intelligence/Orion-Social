import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import ChessComConstants

constants = ChessComConstants


def probe_url(username: str) -> str:
    return ChessComConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(payload.get("name") or payload.get("username")),
        "username": parse.text(payload.get("username")),
        "avatar": parse.text(payload.get("avatar")),
        "id": parse.text(payload.get("player_id")),
        "followers": parse.text(payload.get("followers")),
        "created_at": parse.text(payload.get("joined")),
        "last_online": parse.text(payload.get("last_online")),
        "title": parse.text(payload.get("title")),
        "location": parse.clean(payload.get("location")),
        "country": parse.text(payload.get("country")).rstrip("/").split("/")[-1],
        "status": parse.text(payload.get("status")),
        "league": parse.text(payload.get("league")),
        "twitch": parse.text(payload.get("twitch_url")),
        "verified": "true" if payload.get("verified") else "",
        "streamer": "true" if payload.get("is_streamer") else "",
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
    ("member/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("club/(?P<id>[^/]+)(?:/.*)?", "group"),
)
