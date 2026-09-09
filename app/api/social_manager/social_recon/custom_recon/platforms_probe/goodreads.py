import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GoodreadsConstants

constants = GoodreadsConstants


def probe_url(username: str) -> str:
    return GoodreadsConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in GoodreadsConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, GoodreadsConstants.AVATAR_KEYS, GoodreadsConstants.COVER_KEYS)
    if info.get("display_name"):
        info["display_name"] = parse.clean(info["display_name"])
    if info.get("description"):
        info["description"] = parse.clean(info["description"])
    username = re.search(GoodreadsConstants.TITLE_USERNAME, heading)
    if username and username.group(1) and "books" not in username.group(1).lower():
        info["username"] = username.group(1).strip()
    location = re.search(GoodreadsConstants.TITLE_LOCATION, heading)
    if location:
        info["location"] = parse.clean(location.group(1))
    books = re.search(GoodreadsConstants.TITLE_BOOKS, heading)
    if books:
        info["books"] = books.group(1)
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
    ("(?:user|author)/show/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("group/show/(?P<id>[^/]+)", "group"),
    ("(?P<id>[^/]+)", "profile"),
)

