import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BilibiliConstants

constants = BilibiliConstants


def probe_url(username: str) -> str:
    return BilibiliConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    return http_client.fetch(BilibiliConstants.API_URL.format(username=username))


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict):
        return VerdictConstants.UNKNOWN, {}
    if payload.get("code") == -404:
        return VerdictConstants.ABSENT, {}
    data = payload.get("data")
    if payload.get("code") != 0 or not isinstance(data, dict):
        return VerdictConstants.UNKNOWN, {}
    card = data.get("card") if isinstance(data.get("card"), dict) else {}
    space = data.get("space") if isinstance(data.get("space"), dict) else {}
    level = card.get("level_info") if isinstance(card.get("level_info"), dict) else {}
    info = {
        "display_name": parse.clean(card.get("name")),
        "description": parse.clean(card.get("sign") or card.get("description")),
        "avatar": parse.text(card.get("face")),
        "cover": parse.text(space.get("l_img") or space.get("s_img")),
        "id": parse.text(card.get("mid")),
        "followers": parse.text(data.get("follower") or card.get("fans")),
        "following": parse.text(card.get("attention")),
        "gender": parse.text(card.get("sex")),
        "location": parse.clean(card.get("place")),
        "level": parse.text(level.get("current_level")) if level.get("current_level") else "",
        "videos": parse.text(data.get("archive_count")) if data.get("archive_count") else "",
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

HOSTS = ("bilibili.com", "b23.tv")
ROUTES = (
    (r"(?P<id>\d+)(?:/.*)?", "profile"),
)

