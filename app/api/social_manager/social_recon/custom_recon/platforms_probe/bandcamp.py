import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BandcampConstants

constants = BandcampConstants


def probe_url(username: str) -> str:
    return BandcampConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in BandcampConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    meta = parse.meta(body)
    entity = parse.ld_entity(body, "MusicGroup", "MusicAlbum", "MusicRecording", "MusicPlaylist")
    group = entity if str(entity.get("@type", "")).endswith("Group") else entity.get("publisher") or entity.get("byArtist") or {}
    if not isinstance(group, dict):
        group = {}
    info = {
        "display_name": parse.clean(meta.get("og:site_name") or group.get("name")),
        "avatar": parse.text(group.get("image")),
    }
    if parse.is_generic_image(info["avatar"]):
        info["avatar"] = ""
    for prop in group.get("additionalProperty") or []:
        if isinstance(prop, dict) and prop.get("name") == "band_id" and prop.get("value"):
            info["id"] = parse.text(prop.get("value"))
    for name, link in parse.social_links(group.get("sameAs")).items():
        info.setdefault(name, link)
    if not info["display_name"]:
        return VerdictConstants.EXISTS, parse.social_info(body, BandcampConstants.AVATAR_KEYS, BandcampConstants.COVER_KEYS)
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

HOSTS = ("bandcamp.com",)
SUBDOMAIN = ("bandcamp.com", "profile")
ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)

