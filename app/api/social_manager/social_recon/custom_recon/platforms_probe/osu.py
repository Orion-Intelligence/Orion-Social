import html
import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import OsuConstants

constants = OsuConstants


def probe_url(username: str) -> str:
    return OsuConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in OsuConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    match = re.search(OsuConstants.INITIAL_DATA, body)
    user = (parse.as_json(html.unescape(match.group(1))) or {}).get("user") if match else None
    if not isinstance(user, dict) or not user.get("username"):
        return VerdictConstants.EXISTS, parse.social_info(body, OsuConstants.AVATAR_KEYS, OsuConstants.COVER_KEYS)
    stats = user.get("statistics") if isinstance(user.get("statistics"), dict) else {}
    info = {
        "display_name": parse.clean(user.get("username")),
        "username": parse.text(user.get("username")),
        "avatar": parse.text(user.get("avatar_url")),
        "cover": parse.text(user.get("cover_url")),
        "id": parse.text(user.get("id")),
        "country": parse.text(user.get("country_code")),
        "location": parse.clean(user.get("location")),
        "created_at": parse.text(user.get("join_date")),
        "followers": parse.text(user.get("follower_count")) if user.get("follower_count") else "",
        "discord": parse.text(user.get("discord")),
        "pp": parse.text(stats.get("pp")) if stats.get("pp") else "",
        "rank": parse.text(stats.get("global_rank")) if stats.get("global_rank") else "",
        "play_count": parse.text(stats.get("play_count")) if stats.get("play_count") else "",
        "supporter": "true" if user.get("is_supporter") else "",
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
    ("(?:users|u)/(?P<id>[^/]+)(?:/.*)?", "profile"),
)

