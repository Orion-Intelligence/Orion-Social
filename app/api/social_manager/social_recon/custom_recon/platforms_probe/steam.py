import re

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import SteamCommunityConstants

constants = SteamCommunityConstants


def probe_url(username: str) -> str:
    return SteamCommunityConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    return http_client.fetch(SteamCommunityConstants.XML_URL.format(username=username))


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    if "<error>" in body:
        return VerdictConstants.ABSENT, {}

    def first(tag: str) -> str:
        match = re.search(SteamCommunityConstants.XML_FIELD.format(tag=tag), body, re.DOTALL)
        return match.group(1).strip() if match else ""

    if not first("steamID64"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(first("steamID")),
        "username": parse.text(first("customURL")) or parse.text(_final_url).rstrip("/").split("/")[-1].split("?")[0],
        "description": parse.clean(first("summary")),
        "avatar": parse.text(first("avatarFull") or first("avatarMedium")),
        "id": parse.text(first("steamID64")),
        "realname": parse.clean(first("realname")),
        "location": parse.clean(first("location")),
        "created_at": parse.clean(first("memberSince")),
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
    ("(?:id|profiles)/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("groups/(?P<id>[^/]+)(?:/.*)?", "group"),
)

