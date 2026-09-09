import json

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import AniListConstants

constants = AniListConstants


def probe_url(username: str) -> str:
    return AniListConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    payload = json.dumps({"query": AniListConstants.GQL_QUERY, "variables": {"name": username}})
    return http_client.post(AniListConstants.GQL_URL, payload, {"Content-Type": "application/json", "Accept": "application/json"})


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    user = (payload.get("data") or {}).get("User") if isinstance(payload, dict) else None
    if not isinstance(user, dict) or not user.get("id"):
        return VerdictConstants.UNKNOWN, {}
    avatar = user.get("avatar") if isinstance(user.get("avatar"), dict) else {}
    stats = user.get("statistics") if isinstance(user.get("statistics"), dict) else {}
    anime = stats.get("anime") if isinstance(stats.get("anime"), dict) else {}
    manga = stats.get("manga") if isinstance(stats.get("manga"), dict) else {}
    info = {
        "display_name": parse.text(user.get("name")),
        "description": parse.clean(user.get("about")),
        "avatar": parse.text(avatar.get("large") or avatar.get("medium")),
        "cover": parse.text(user.get("bannerImage")),
        "id": parse.text(user.get("id")),
        "created_at": parse.text(user.get("createdAt")),
        "updated_at": parse.text(user.get("updatedAt")),
        "donator_tier": parse.text(user.get("donatorTier")) if user.get("donatorTier") else "",
        "donator_badge": parse.text(user.get("donatorBadge")),
        "anime_count": parse.text(anime.get("count")) if anime.get("count") else "",
        "manga_count": parse.text(manga.get("count")) if manga.get("count") else "",
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
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)

