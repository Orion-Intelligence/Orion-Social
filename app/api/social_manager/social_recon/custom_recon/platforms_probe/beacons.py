import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BeaconsConstants

constants = BeaconsConstants


def probe_url(username: str) -> str:
    return BeaconsConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in BeaconsConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, BeaconsConstants.AVATAR_KEYS, BeaconsConstants.COVER_KEYS)
    match = re.match(BeaconsConstants.HANDLE, parse.text(parse.meta(body).get("og:title")))
    if match:
        info["username"] = match.group(1)
        info["display_name"] = match.group(1)
    bio = info.get("description", "")
    for marker in BeaconsConstants.BIO_TRIM:
        bio = bio.split(marker)[0]
    bio = parse.clean(bio.replace("##", " ").rstrip(" .:"))
    info["description"] = "" if any(token in bio.casefold() for token in BeaconsConstants.BIO_DEFAULT) else bio
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
