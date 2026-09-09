import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import TikTokConstants

constants = TikTokConstants


def probe_url(username: str) -> str:
    return TikTokConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status in (400, 404):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.embedded_object(body, TikTokConstants.DATA_KEY)
    user = payload.get("user") if isinstance(payload.get("user"), dict) else {}
    stats = payload.get("stats") if isinstance(payload.get("stats"), dict) else {}
    if not user.get("uniqueId"):
        lowered = body.casefold()
        if any(marker.casefold() in lowered for marker in TikTokConstants.NOT_FOUND):
            return VerdictConstants.ABSENT, {}
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(user.get("nickname")),
        "username": parse.text(user.get("uniqueId")),
        "description": parse.clean(user.get("signature")),
        "avatar": parse.text(user.get("avatarLarger") or user.get("avatarMedium")),
        "id": parse.text(user.get("id")),
        "region": parse.text(user.get("region")),
        "verified": "true" if user.get("verified") else "",
        "followers": parse.text(stats.get("followerCount")) if stats.get("followerCount") else "",
        "following": parse.text(stats.get("followingCount")) if stats.get("followingCount") else "",
        "likes": parse.text(stats.get("heartCount")) if stats.get("heartCount") else "",
        "videos": parse.text(stats.get("videoCount")) if stats.get("videoCount") else "",
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
    (r"@(?P<id>[^/]+)", "profile"),
)

