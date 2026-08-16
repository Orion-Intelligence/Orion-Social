import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GIPHYConstants

constants = GIPHYConstants


def probe_url(username: str) -> str:
    return GIPHYConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in GIPHYConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, GIPHYConstants.AVATAR_KEYS, GIPHYConstants.COVER_KEYS)

ROUTES = (
    ("(?:gifs|stickers)/(?P<id>[^/]+)", "post"),
    ("(?:channel/)?(?P<id>[^/]+)", "profile"),
)
