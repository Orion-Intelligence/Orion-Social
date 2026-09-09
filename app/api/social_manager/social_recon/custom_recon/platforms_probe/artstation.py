import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import ArtStationConstants

constants = ArtStationConstants


def probe_url(username: str) -> str:
    return ArtStationConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    return http_client.fetch(ArtStationConstants.API_URL.format(username=username))


def _image(url: object) -> str:
    value = parse.text(url)
    return "" if parse.is_generic_image(value) else value


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    data = parse.as_json(body)
    if not isinstance(data, dict) or not (data.get("username") or data.get("id")):
        return VerdictConstants.UNKNOWN, {}
    location = ", ".join(part for part in (parse.text(data.get("city")), parse.text(data.get("country"))) if part)
    info = {
        "display_name": parse.clean(data.get("full_name")),
        "username": parse.text(data.get("username")),
        "description": parse.clean(data.get("headline")),
        "avatar": _image(data.get("large_avatar_url") or data.get("medium_avatar_url")),
        "cover": _image(data.get("default_cover_url")),
        "id": parse.text(data.get("id")),
        "location": location,
        "followers": parse.text(data.get("followers_count")) if data.get("followers_count") else "",
        "following": parse.text(data.get("followees_count")) if data.get("followees_count") else "",
        "posts": parse.text(data.get("projects_count")) if data.get("projects_count") else "",
        "pro": "true" if data.get("pro_member") or data.get("is_plus_member") else "",
    }
    for source, target in ArtStationConstants.SOCIAL_KEYS.items():
        value = parse.text(data.get(source))
        if value and not info.get(target):
            info[target] = value
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

