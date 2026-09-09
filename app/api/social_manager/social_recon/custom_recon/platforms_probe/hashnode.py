import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import HashnodeConstants

constants = HashnodeConstants


def probe_url(username: str) -> str:
    return HashnodeConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in HashnodeConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    name = parse.clean(heading.split(HashnodeConstants.NAME_SPLIT)[0])
    description = parse.clean(parse.meta(body).get("og:description", "").split(HashnodeConstants.DESC_TRIM)[0].rstrip(" ."))
    info = {"display_name": name, "description": description}
    handle = re.search(HashnodeConstants.HANDLE, heading)
    if handle:
        info["username"] = handle.group(1)
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("@(?P<id>[^/]+)(?:/.*)?", "profile"),
)
