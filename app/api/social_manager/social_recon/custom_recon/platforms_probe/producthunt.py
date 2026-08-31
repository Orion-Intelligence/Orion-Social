import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import ProductHuntConstants

constants = ProductHuntConstants


def probe_url(username: str) -> str:
    return ProductHuntConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    return http_client.fetch(probe_url(username), impersonate=ProductHuntConstants.IMPERSONATE)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in ProductHuntConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, ProductHuntConstants.AVATAR_KEYS, ProductHuntConstants.COVER_KEYS)

ROUTES = (
    ("@(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("(?:posts|products)/(?P<id>[^/]+)(?:/.*)?", "post"),
)
