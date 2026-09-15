import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import CoddyConstants

constants = CoddyConstants


def probe_url(username: str) -> str:
    return CoddyConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in getattr(CoddyConstants, "GENERIC", set()):
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, getattr(CoddyConstants, "AVATAR_KEYS", ()), getattr(CoddyConstants, "COVER_KEYS", ()))
    person = parse.ld_entity(body, "Person", "ProfilePage")
    if not info.get("display_name") and person.get("name"):
        info["display_name"] = person.get("name")
    if not info.get("description") and person.get("description"):
        info["description"] = person.get("description")
    if info.get("display_name"):
        info["display_name"] = parse.clean(re.split(r"\s+[-|—]\s+", info["display_name"], maxsplit=1)[0])
    if info.get("display_name") and info["display_name"].casefold() in getattr(CoddyConstants, "GENERIC", set()):
        return VerdictConstants.UNKNOWN, {}
    if info.get("description"):
        info["description"] = parse.clean(info["description"])
    if not any(info.get(key) for key in ("display_name", "avatar", "description")):
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


ROUTES = (
    (r"user/(?P<id>[^/]+)", "profile"),
)
