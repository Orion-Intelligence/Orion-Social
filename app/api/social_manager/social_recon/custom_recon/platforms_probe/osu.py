import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import OsuConstants

constants = OsuConstants


def probe_url(username: str) -> str:
    return OsuConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in OsuConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, OsuConstants.AVATAR_KEYS, OsuConstants.COVER_KEYS)

ROUTES = (
    ("(?:users|u)/(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"beatmapsets/(?P<id>\d+)(?:/.*)?", "post"),
)
