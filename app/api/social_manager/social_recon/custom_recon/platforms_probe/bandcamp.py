import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BandcampConstants

constants = BandcampConstants


def probe_url(username: str) -> str:
    return BandcampConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in BandcampConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, BandcampConstants.AVATAR_KEYS, BandcampConstants.COVER_KEYS)

HOSTS = ("bandcamp.com",)
SUBDOMAIN = ("bandcamp.com", "profile")
ROUTES = (
    ("(?:album|track)/(?P<id>[^/]+)", "post"),
    ("(?P<id>[^/]+)", "profile"),
)
