import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import AcademiaEduConstants

constants = AcademiaEduConstants


def probe_url(username: str) -> str:
    return AcademiaEduConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in AcademiaEduConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, AcademiaEduConstants.AVATAR_KEYS, AcademiaEduConstants.COVER_KEYS)
    person = parse.ld_entity(body, "Person", "ProfilePage")
    if not info.get("display_name"):
        info["display_name"] = parse.clean(person.get("name"))
    if not info.get("description"):
        info["description"] = parse.clean(person.get("description"))
    info["created_at"] = parse.text(person.get("dateCreated"))
    match = re.search(AcademiaEduConstants.INTERESTS, body, re.DOTALL)
    if match:
        interests = parse.as_json(match.group(1)) or []
        names = [parse.clean(item.get("name")) for item in interests if isinstance(item, dict) and item.get("name")]
        if names:
            info["interests"] = ", ".join(names[: AcademiaEduConstants.MAX_INTERESTS])
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

SUBDOMAIN = ("academia.edu", "page")
ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)


