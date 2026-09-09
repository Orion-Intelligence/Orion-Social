import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import OpenSeaConstants

constants = OpenSeaConstants


def probe_url(username: str) -> str:
    return OpenSeaConstants.PROFILE_URL.format(username=username)


def _image(url: str) -> str:
    value = parse.text(url)
    return "" if parse.is_generic_image(value) else value


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    profile = parse.embedded_object(body, OpenSeaConstants.DATA_KEY)
    if not (isinstance(profile, dict) and (profile.get("username") or profile.get("address"))):
        heading = parse.title(body)
        if not heading or heading.casefold() in OpenSeaConstants.GENERIC:
            return VerdictConstants.UNKNOWN, {}
        return VerdictConstants.EXISTS, parse.social_info(body)
    info = {
        "display_name": parse.text(profile.get("displayName") or profile.get("username")),
        "username": parse.text(profile.get("username")),
        "bio": parse.text(profile.get("bio")),
        "avatar": _image(profile.get("imageUrl")),
        "cover": _image(profile.get("bannerImageUrl")),
        "address": parse.text(profile.get("address")),
        "account_id": parse.text(profile.get("accountId")),
        "created_at": parse.text(profile.get("dateJoined")),
        "website": parse.text(profile.get("externalUrl")),
        "ens_name": parse.text(profile.get("ensName")),
        "twitter": parse.text(profile.get("twitterUsername")),
        "instagram": parse.text(profile.get("instagramUsername")),
        "followers": parse.text(profile.get("followerCount")),
        "following": parse.text(profile.get("followingCount")),
        "verified": "true" if (profile.get("isVerified") or profile.get("profileIsVerified")) else "",
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
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)

