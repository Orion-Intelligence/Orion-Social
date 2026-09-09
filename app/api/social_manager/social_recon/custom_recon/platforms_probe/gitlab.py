import re
import urllib.parse

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GitLabConstants

constants = GitLabConstants


def probe_url(username: str) -> str:
    return GitLabConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, list):
        return VerdictConstants.UNKNOWN, {}
    if not payload:
        return VerdictConstants.ABSENT, {}
    user = payload[0] if isinstance(payload[0], dict) else {}
    if not user.get("username"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(user.get("name")),
        "username": parse.text(user.get("username")),
        "avatar": parse.text(user.get("avatar_url")),
        "id": parse.text(user.get("id")),
        "website": parse.text(user.get("web_url")),
        "email": parse.text(user.get("public_email")),
        "state": parse.text(user.get("state")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    match = re.search(GitLabConstants.PROJECT_RE, final_url or "")
    path = match.group(1).split("/-/")[0].split("?")[0].split("#")[0].strip("/") if match else ""
    if path and "/" in path:
        encoded = urllib.parse.quote(path, safe="")
        code, payload, _ = http_client.fetch(GitLabConstants.PROJECT_API.format(path=encoded))
        if code == 404:
            return VerdictConstants.ABSENT, {}
        data = parse.as_json(payload) if code == 200 else None
        if isinstance(data, dict) and data.get("path_with_namespace"):
            topics = data.get("topics") if isinstance(data.get("topics"), list) else []
            info = {
                "title": parse.text(data.get("name")),
                "path": parse.text(data.get("path_with_namespace")),
                "description": parse.clean(data.get("description")),
                "stars": parse.text(data.get("star_count")) if data.get("star_count") else "",
                "forks": parse.text(data.get("forks_count")) if data.get("forks_count") else "",
                "topics": ", ".join(topics),
                "visibility": parse.text(data.get("visibility")),
                "created_at": parse.text(data.get("created_at")),
                "updated_at": parse.text(data.get("last_activity_at")),
            }
            return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
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
    ("groups/(?P<id>[^/]+)(?:/.*)?", "group"),
    ("(?P<id>[^/]+)/(?P<repo>[^/]+)(?:/.*)?", "repo"),
    ("(?P<id>[^/]+)", "profile"),
)
