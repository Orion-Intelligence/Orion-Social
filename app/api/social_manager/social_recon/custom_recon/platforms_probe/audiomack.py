import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import AudiomackConstants

constants = AudiomackConstants


def probe_url(username: str) -> str:
    return AudiomackConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in AudiomackConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, AudiomackConstants.AVATAR_KEYS, AudiomackConstants.COVER_KEYS)
    group = parse.ld_entity(body, "MusicGroup")
    if group:
        if group.get("name"):
            info["display_name"] = parse.clean(group.get("name"))
        if group.get("description"):
            info["description"] = parse.clean(group.get("description"))
        if not info.get("avatar"):
            info["avatar"] = parse.text(group.get("image"))
        info["genre"] = parse.text(group.get("genre"))
        location = group.get("location") if isinstance(group.get("location"), dict) else {}
        info["location"] = parse.clean(location.get("name"))
        for stat in group.get("interactionStatistic") or []:
            if not isinstance(stat, dict):
                continue
            kind = stat.get("interactionType")
            kind = kind.get("@type") if isinstance(kind, dict) else kind
            if "Listen" in str(kind) and stat.get("userInteractionCount"):
                info["plays"] = parse.text(stat.get("userInteractionCount"))
        for name, link in parse.social_links(group.get("sameAs")).items():
            info.setdefault(name, link)
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
    ("(?P<id>[^/]+)", "profile"),
)

