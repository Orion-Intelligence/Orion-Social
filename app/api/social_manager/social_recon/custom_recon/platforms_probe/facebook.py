import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import FacebookConstants

constants = FacebookConstants


def probe_url(username: str) -> str:
    return FacebookConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in FacebookConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, FacebookConstants.AVATAR_KEYS, FacebookConstants.COVER_KEYS)
    if re.search(FacebookConstants.PAGE_PATTERN, info.get("description", ""), flags=re.IGNORECASE):
        info["target_type"] = "page"
    return VerdictConstants.EXISTS, info

ROUTES = (
    (r"groups/(?P<id>[^/]+)(?:/.*)?", "group"),
    (r"(?P<id>[^/]+)/posts/[^/]+", "post"),
    (r"profile\.php\?id=(?P<id>\d+)", "profile"),
    (r"(?P<id>[^/]+)", "profile"),
)
