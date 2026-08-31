import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import WellfoundConstants

constants = WellfoundConstants


def probe_url(username: str) -> str:
    return WellfoundConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in WellfoundConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, WellfoundConstants.AVATAR_KEYS, WellfoundConstants.COVER_KEYS)

HOSTS = ("angel.co",)
ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("company/(?P<id>[^/]+)(?:/.*)?", "page"),
)
