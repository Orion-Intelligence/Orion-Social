import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.custom_recon_constants import CrawlConstants, VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import XConstants

constants = XConstants


def probe_url(username: str) -> str:
    if XConstants.CRAWL_TYPE == CrawlConstants.PLAYWRIGHT:
        return XConstants.PROFILE_URL.format(username=username)
    return XConstants.SYNDICATION_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    user = {}
    if isinstance(payload, dict):
        props = (payload.get("props") or {}).get("pageProps") or {}
        user = props.get("user") or {}
    if not user:
        heading = parse.title(body)
        if not heading or heading.casefold() in XConstants.GENERIC:
            return VerdictConstants.UNKNOWN, {}
        return VerdictConstants.EXISTS, parse.social_info(body)
    info = {
        "display_name": parse.clean(user.get("name")),
        "username": parse.text(user.get("screen_name")),
        "description": parse.clean(user.get("description")),
        "avatar": parse.text(user.get("profile_image_url_https")),
        "cover": parse.text(user.get("profile_banner_url")),
        "followers": parse.text(user.get("followers_count")) if user.get("followers_count") else "",
        "following": parse.text(user.get("friends_count")) if user.get("friends_count") else "",
        "posts": parse.text(user.get("statuses_count")) if user.get("statuses_count") else "",
        "location": parse.clean(user.get("location")),
        "id": parse.text(user.get("id_str")),
        "created_at": parse.text(user.get("created_at")),
        "verified": "true" if user.get("verified") or user.get("is_blue_verified") else "",
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

