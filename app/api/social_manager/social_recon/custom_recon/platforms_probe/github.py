import re

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GitHubConstants

constants = GitHubConstants


def probe_url(username: str) -> str:
    return GitHubConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or not payload.get("login"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(payload.get("name")),
        "username": parse.text(payload.get("login")),
        "description": parse.clean(payload.get("bio")),
        "avatar": parse.text(payload.get("avatar_url")),
        "id": parse.text(payload.get("id")),
        "followers": parse.text(payload.get("followers")) if payload.get("followers") else "",
        "following": parse.text(payload.get("following")) if payload.get("following") else "",
        "repos": parse.text(payload.get("public_repos")) if payload.get("public_repos") else "",
        "created_at": parse.text(payload.get("created_at")),
        "updated_at": parse.text(payload.get("updated_at")),
        "location": parse.clean(payload.get("location")),
        "company": parse.clean(payload.get("company")),
        "website": parse.text(payload.get("blog")),
        "twitter": parse.text(payload.get("twitter_username")),
        "type": parse.text(payload.get("type")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    match = re.search(GitHubConstants.REPO_RE, final_url or "")
    if match:
        owner, repo = match.group(1), match.group(2)
        code, payload, _ = http_client.fetch(GitHubConstants.REPO_API.format(owner=owner, repo=repo))
        if code == 404:
            return VerdictConstants.ABSENT, {}
        data = parse.as_json(payload) if code == 200 else None
        if isinstance(data, dict) and data.get("full_name"):
            topics = data.get("topics") if isinstance(data.get("topics"), list) else []
            info = {
                "title": parse.text(data.get("full_name")),
                "description": parse.clean(data.get("description")),
                "owner": parse.text((data.get("owner") or {}).get("login")),
                "language": parse.text(data.get("language")),
                "stars": parse.text(data.get("stargazers_count")) if data.get("stargazers_count") else "",
                "forks": parse.text(data.get("forks_count")) if data.get("forks_count") else "",
                "open_issues": parse.text(data.get("open_issues_count")) if data.get("open_issues_count") else "",
                "topics": ", ".join(topics),
                "license": parse.text((data.get("license") or {}).get("name")),
                "website": parse.text(data.get("homepage")),
                "created_at": parse.text(data.get("created_at")),
                "updated_at": parse.text(data.get("updated_at")),
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
    ("orgs/(?P<id>[^/]+)(?:/.*)?", "page"),
    ("(?P<id>[^/]+)/(?P<repo>[^/]+)(?:/.*)?", "repo"),
    ("(?P<id>[^/]+)", "profile"),
)
