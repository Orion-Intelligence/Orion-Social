import re

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import ScratchConstants

constants = ScratchConstants


def probe_url(username: str) -> str:
    return ScratchConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}
    images = profile.get("images") if isinstance(profile.get("images"), dict) else {}
    info = {
        "display_name": parse.text(payload.get("username")),
        "username": parse.text(payload.get("username")),
        "description": parse.clean(profile.get("bio")),
        "avatar": parse.text(images.get("90x90")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text((payload.get("history") or {}).get("joined")),
        "location": parse.clean(profile.get("country")),
        "scratchteam": "true" if payload.get("scratchteam") else "",
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    project = re.search(r"/projects/(\d+)", final_url or "")
    studio = re.search(r"/studios/(\d+)", final_url or "")
    if project:
        code, payload, _ = http_client.fetch(ScratchConstants.PROJECT_API.format(id=project.group(1)))
        if code == 404:
            return VerdictConstants.ABSENT, {}
        data = parse.as_json(payload) if code == 200 else None
        if isinstance(data, dict) and data.get("id"):
            stats = data.get("stats") if isinstance(data.get("stats"), dict) else {}
            info = {
                "title": parse.clean(data.get("title")),
                "description": parse.clean(data.get("description")),
                "author": parse.text((data.get("author") or {}).get("username")),
                "image": parse.text(data.get("image")),
                "views": parse.text(stats.get("views")) if stats.get("views") else "",
                "loves": parse.text(stats.get("loves")) if stats.get("loves") else "",
                "favorites": parse.text(stats.get("favorites")) if stats.get("favorites") else "",
                "remixes": parse.text(stats.get("remixes")) if stats.get("remixes") else "",
                "created_at": parse.text((data.get("history") or {}).get("created")),
            }
            return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
    if studio:
        code, payload, _ = http_client.fetch(ScratchConstants.STUDIO_API.format(id=studio.group(1)))
        if code == 404:
            return VerdictConstants.ABSENT, {}
        data = parse.as_json(payload) if code == 200 else None
        if isinstance(data, dict) and data.get("id"):
            stats = data.get("stats") if isinstance(data.get("stats"), dict) else {}
            info = {
                "title": parse.clean(data.get("title")),
                "description": parse.clean(data.get("description")),
                "host": parse.text(data.get("host")),
                "followers": parse.text(stats.get("followers")) if stats.get("followers") else "",
                "created_at": parse.text((data.get("history") or {}).get("created")),
            }
            return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
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
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"studios/(?P<id>\d+)(?:/.*)?", "group"),
)

