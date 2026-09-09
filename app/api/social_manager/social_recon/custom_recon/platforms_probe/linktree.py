import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import LinktreeConstants

constants = LinktreeConstants


def probe_url(username: str) -> str:
    return LinktreeConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in LinktreeConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    avatar = parse.json_url(body, *LinktreeConstants.AVATAR_KEYS)
    info = {
        "username": parse.text(parse.meta(body).get("og:url")).rstrip("/").split("/")[-1],
        "avatar": "" if parse.is_generic_image(avatar) else avatar,
    }
    links = [link.replace("\\u0026", "&").replace("\\/", "/") for link in re.findall(LinktreeConstants.SOCIAL_LINKS, body)]
    for name, link in parse.social_links(links).items():
        info.setdefault(name, link)
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
