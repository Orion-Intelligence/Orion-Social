import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import LetterboxdConstants

constants = LetterboxdConstants


def probe_url(username: str) -> str:
    return LetterboxdConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in LetterboxdConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    meta = parse.meta(body)
    info = parse.social_info(body, LetterboxdConstants.AVATAR_KEYS, LetterboxdConstants.COVER_KEYS)
    name = re.match(LetterboxdConstants.NAME_RE, parse.text(meta.get("og:title")))
    if name:
        info["display_name"] = parse.clean(name.group(1))
    handle = parse.text(meta.get("og:url")).rstrip("/").split("/")[-1]
    if handle:
        info["username"] = handle
    description = parse.text(meta.get("og:description"))
    films = re.search(LetterboxdConstants.FILMS, description)
    if films:
        info["films_watched"] = films.group(1)
    favorites = re.search(LetterboxdConstants.FAVORITES, description)
    if favorites:
        info["favorites"] = parse.clean(favorites.group(1))
    bio = re.search(LetterboxdConstants.BIO, description)
    info["description"] = parse.clean(bio.group(1)) if bio else ""
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
    ("(?P<id>[^/]+/list/[^/]+)(?:/.*)?", "group"),
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)


