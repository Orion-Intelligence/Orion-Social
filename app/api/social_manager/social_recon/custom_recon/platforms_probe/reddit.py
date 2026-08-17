import re
from html import unescape

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import CrawlConstants, VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import RedditConstants

constants = RedditConstants


def probe_url(username: str) -> str:
    if RedditConstants.CRAWL_TYPE == CrawlConstants.PLAYWRIGHT:
        return RedditConstants.PROFILE_URL.format(username=username)
    return RedditConstants.ABOUT_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict):
        if RedditConstants.MISSING_USER in body:
            return VerdictConstants.ABSENT, {}
        heading = parse.title(body)
        if not heading or heading.casefold() in RedditConstants.GENERIC:
            return VerdictConstants.UNKNOWN, {}
        info = parse.social_info(body)
        info.setdefault("avatar", parse.first_image(body))
        return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
    data = payload.get("data")
    if not isinstance(data, dict) or not data.get("name"):
        return VerdictConstants.UNKNOWN, {}
    profile = data.get("subreddit") if isinstance(data.get("subreddit"), dict) else {}
    info = {
        "display_name": parse.text(data.get("name")),
        "avatar": parse.text(data.get("icon_img") or profile.get("icon_img")).split("?")[0],
        "cover": parse.text(profile.get("banner_img")).split("?")[0],
        "id": parse.text(data.get("id")),
        "created_at": parse.text(data.get("created_utc")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}



def evaluate_resource(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    if not any(marker in body for marker in RedditConstants.RESOURCE_MARKERS):
        heading = parse.title(body)
        return (VerdictConstants.ABSENT, {}) if not heading or heading.casefold() in RedditConstants.GENERIC else (VerdictConstants.UNKNOWN, {})
    info = parse.social_info(body)
    match = re.search(RedditConstants.RESOURCE_DESCRIPTION, body or "", flags=re.IGNORECASE | re.DOTALL)
    if match and not info.get("description"):
        info["description"] = re.sub(r"\s+", " ", unescape(match.group(1))).strip()
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    (r"(?:user|u)/(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"r/[^/]+/comments/(?P<id>[^/]+)(?:/.*)?", "post"),
    (r"r/(?P<id>[^/]+)(?:/.*)?", "subreddit"),
)
