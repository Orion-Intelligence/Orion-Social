import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import InstagramConstants

constants = InstagramConstants


def probe_url(username: str) -> str:
    return InstagramConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in InstagramConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    meta = parse.meta(body)
    info = parse.social_info(body, InstagramConstants.AVATAR_KEYS, InstagramConstants.COVER_KEYS)
    counts = parse.counts(parse.text(meta.get("og:description")) or info.get("description", ""))
    info.update({key: counts[key] for key in ("followers", "following", "posts") if key in counts})
    if "threads" in counts:
        info.setdefault("posts", counts["threads"])
    info["display_name"] = parse.clean(parse.text(meta.get("og:title")).split(InstagramConstants.NAME_SPLIT)[0]) or info.get("display_name", "")
    handle = re.search(InstagramConstants.HANDLE, parse.text(meta.get("og:title")))
    if handle:
        info["username"] = handle.group(1)
    description = parse.text(meta.get("description"))
    info["description"] = parse.clean(description.split(InstagramConstants.BIO_SPLIT, 1)[1].rstrip('"')) if InstagramConstants.BIO_SPLIT in description else ""
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

