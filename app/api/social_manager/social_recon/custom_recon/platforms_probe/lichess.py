import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import LichessConstants

constants = LichessConstants


def probe_url(username: str) -> str:
    return LichessConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and (payload.get("closed") or payload.get("disabled")):
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}
    count = payload.get("count") if isinstance(payload.get("count"), dict) else {}
    streamer = payload.get("streamer") if isinstance(payload.get("streamer"), dict) else {}
    info = {
        "display_name": parse.clean(profile.get("realName") or payload.get("username")),
        "username": parse.text(payload.get("username")),
        "description": parse.clean(profile.get("bio")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text(payload.get("createdAt")),
        "last_online": parse.text(payload.get("seenAt")),
        "location": parse.clean(profile.get("location")),
        "country": parse.text(profile.get("country") or profile.get("flag")),
        "games": parse.text(count.get("all")) if count.get("all") else "",
        "title": parse.text(payload.get("title")),
        "verified": "true" if payload.get("verified") else "",
        "patron": "true" if payload.get("patron") else "",
    }
    twitch = (streamer.get("twitch") or {}).get("channel") if isinstance(streamer.get("twitch"), dict) else None
    if twitch:
        info["twitch"] = parse.text(twitch)
    raw_links = profile.get("links")
    link_list = raw_links.splitlines() if isinstance(raw_links, str) else (raw_links if isinstance(raw_links, list) else [])
    normalized = [item if str(item).startswith("http") else f"https://{str(item).strip()}" for item in link_list if str(item).strip()]
    for name, link in parse.social_links(normalized).items():
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
    ("@/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("team/(?P<id>[^/]+)(?:/.*)?", "group"),
)
