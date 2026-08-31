import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BehanceConstants

constants = BehanceConstants


def probe_url(username: str) -> str:
    return BehanceConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    return http_client.fetch(probe_url(username), impersonate=BehanceConstants.IMPERSONATE)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in BehanceConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, BehanceConstants.AVATAR_KEYS, BehanceConstants.COVER_KEYS)

ROUTES = (
    (r"gallery/(?P<id>\d+)(?:/.*)?", "post"),
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
