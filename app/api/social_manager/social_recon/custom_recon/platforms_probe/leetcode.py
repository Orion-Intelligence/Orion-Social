import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import LeetCodeConstants

constants = LeetCodeConstants


def probe_url(username: str) -> str:
    return LeetCodeConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in LeetCodeConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, LeetCodeConstants.AVATAR_KEYS, LeetCodeConstants.COVER_KEYS)

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("problems/(?P<id>[^/]+)(?:/.*)?", "question"),
    ("(?P<id>[^/]+)", "profile"),
)
