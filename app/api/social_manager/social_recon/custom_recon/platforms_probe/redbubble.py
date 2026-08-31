import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import RedbubbleConstants

constants = RedbubbleConstants


def probe_url(username: str) -> str:
    return RedbubbleConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in RedbubbleConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, RedbubbleConstants.AVATAR_KEYS, RedbubbleConstants.COVER_KEYS)

ROUTES = (
    ("people/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("i/[^/]+/(?P<id>[^/]+)(?:/.*)?", "post"),
)
