import re

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import StackOverflowConstants

constants = StackOverflowConstants


def probe_url(username: str) -> str:
    return StackOverflowConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in StackOverflowConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, StackOverflowConstants.AVATAR_KEYS, StackOverflowConstants.COVER_KEYS)
    name = parse.clean(heading)
    if name.startswith("User "):
        name = name[len("User "):]
    name = name.split(" - Stack Overflow")[0].strip()
    if name:
        info["display_name"] = name
    handle = parse.text(_final_url).rstrip("/").split("/")[-1]
    if handle and not handle.isdigit():
        info["username"] = handle
    if info.get("description"):
        info["description"] = parse.clean(info["description"])
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    match = re.search(StackOverflowConstants.QUESTION_RE, final_url or "")
    if match:
        code, payload, _ = http_client.fetch(StackOverflowConstants.QUESTION_API.format(id=match.group(1)))
        data = parse.as_json(payload) if code == 200 else None
        items = data.get("items") if isinstance(data, dict) else None
        if isinstance(items, list) and items:
            item = items[0]
            tags = item.get("tags") if isinstance(item.get("tags"), list) else []
            info = {
                "title": parse.clean(item.get("title")),
                "author": parse.clean((item.get("owner") or {}).get("display_name")),
                "score": parse.text(item.get("score")),
                "answers": parse.text(item.get("answer_count")),
                "views": parse.text(item.get("view_count")),
                "tags": ", ".join(tags),
                "answered": "true" if item.get("is_answered") else "",
                "created_at": parse.text(item.get("creation_date")),
            }
            return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
        if isinstance(data, dict) and not items:
            return VerdictConstants.ABSENT, {}
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
    (r"users/(?P<id>\d+)(?:/.*)?", "profile"),
)

