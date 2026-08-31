import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GumroadConstants

constants = GumroadConstants


def probe_url(username: str) -> str:
    return GumroadConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in GumroadConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, GumroadConstants.AVATAR_KEYS, GumroadConstants.COVER_KEYS)

HOSTS = ("gumroad.com",)
SUBDOMAIN = ("gumroad.com", "profile")
ROUTES = (
    ("l/(?P<id>[^/]+)", "post"),
    ("(?P<id>[a-z0-9-]+)", "profile"),
)
