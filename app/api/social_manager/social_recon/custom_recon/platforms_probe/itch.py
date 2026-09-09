import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import ItchIoConstants

constants = ItchIoConstants


def probe_url(username: str) -> str:
    return ItchIoConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in ItchIoConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, ItchIoConstants.AVATAR_KEYS, ItchIoConstants.COVER_KEYS)
    name = parse.clean(heading)
    if name.endswith(ItchIoConstants.NAME_SUFFIX):
        name = name[: -len(ItchIoConstants.NAME_SUFFIX)].strip()
    if name:
        info["display_name"] = name
        info.setdefault("username", parse.text(_final_url).rstrip("/").split("/")[-1].split(".")[0])
    for name_key, link in parse.social_links(re.findall(ItchIoConstants.REL_ME, body)).items():
        info.setdefault(name_key, link)
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

HOSTS = ("itch.io",)
SUBDOMAIN = ("itch.io", "profile")
ROUTES = (
    ("profile/(?P<id>[^/]+)", "profile"),
)
