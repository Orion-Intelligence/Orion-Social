import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import MastodonConstants

constants = MastodonConstants


def probe_url(username: str) -> str:
    return MastodonConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    return http_client.fetch(MastodonConstants.API_URL.format(username=username))


def _image(url: object) -> str:
    value = parse.text(url)
    return "" if parse.is_generic_image(value) else value


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(payload.get("display_name") or payload.get("username")),
        "username": parse.text(payload.get("username")),
        "description": parse.clean(payload.get("note")),
        "avatar": _image(payload.get("avatar_static") or payload.get("avatar")),
        "cover": _image(payload.get("header_static") or payload.get("header")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text(payload.get("created_at")),
        "followers": parse.text(payload.get("followers_count")) if payload.get("followers_count") else "",
        "following": parse.text(payload.get("following_count")) if payload.get("following_count") else "",
        "posts": parse.text(payload.get("statuses_count")) if payload.get("statuses_count") else "",
        "bot": "true" if payload.get("bot") else "",
    }
    fields = payload.get("fields") if isinstance(payload.get("fields"), list) else []
    links = [link for entry in fields if isinstance(entry, dict) for link in parse.hrefs(entry.get("value"))]
    for name, link in parse.social_links(links).items():
        info.setdefault(name, link)
    if links and not info.get("website"):
        info["website"] = links[0]
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

HOSTS = ("mastodon.online", "mstdn.social", "fosstodon.org", "hachyderm.io")
ROUTES = (
    ("(?:@|users/)(?P<id>[^/@]+)", "profile"),
)

