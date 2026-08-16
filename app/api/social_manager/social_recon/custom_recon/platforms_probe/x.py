import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import CrawlConstants, VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import XConstants

constants = XConstants


def probe_url(username: str) -> str:
    if XConstants.CRAWL_TYPE == CrawlConstants.PLAYWRIGHT:
        return XConstants.PROFILE_URL.format(username=username)
    return XConstants.SYNDICATION_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    user = {}
    if isinstance(payload, dict):
        props = (payload.get("props") or {}).get("pageProps") or {}
        user = props.get("user") or {}
    if not user:
        heading = parse.title(body)
        if not heading or heading.casefold() in XConstants.GENERIC:
            return VerdictConstants.UNKNOWN, {}
        return VerdictConstants.EXISTS, parse.social_info(body)
    info = {
        "display_name": parse.text(user.get("name")),
        "description": parse.text(user.get("description")),
        "avatar": parse.text(user.get("profile_image_url_https")),
        "cover": parse.text(user.get("profile_banner_url")),
        "followers": parse.text(user.get("followers_count")),
        "id": parse.text(user.get("id_str")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    (r"(?P<id>[^/]+)/status/\d+(?:/.*)?", "post"),
    (r"(?P<id>[^/]+)(?:/.*)?", "profile"),
)
