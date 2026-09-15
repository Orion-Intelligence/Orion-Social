import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BeRealConstants

constants = BeRealConstants


def probe_url(username: str) -> str:
    return BeRealConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in getattr(BeRealConstants, "GENERIC", set()):
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, getattr(BeRealConstants, "AVATAR_KEYS", ()), getattr(BeRealConstants, "COVER_KEYS", ()))
    if info.get("display_name"):
        info["display_name"] = parse.clean(re.split(r"\s+on BeReal", info["display_name"], maxsplit=1)[0])
    if info.get("display_name") and info["display_name"].casefold() in getattr(BeRealConstants, "GENERIC", set()):
        info.pop("display_name")
    if info.get("description"):
        info["description"] = parse.clean(info["description"])
    if not info.get("display_name"):
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


ROUTES = (
    (r"(?P<id>[^/]+)", "profile"),
)
