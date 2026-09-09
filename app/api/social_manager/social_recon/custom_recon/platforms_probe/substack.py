import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import SubstackConstants

constants = SubstackConstants


def probe_url(username: str) -> str:
    return SubstackConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in SubstackConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, SubstackConstants.AVATAR_KEYS, SubstackConstants.COVER_KEYS)
    name = parse.clean(parse.text(info.get("display_name") or heading).split(" | Substack")[0])
    if name:
        info["display_name"] = name
    handle = parse.text(parse.meta(body).get("og:url")).rstrip("/").split("/")[-1].lstrip("@")
    if handle:
        info["username"] = handle
    if info.get("description"):
        info["description"] = parse.clean(info["description"])
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

SUBDOMAIN = ("substack.com", "page")
ROUTES = (
    ("@(?P<id>[^/@]+)(?:/.*)?", "profile"),
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
