import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GoodreadsConstants

constants = GoodreadsConstants


def probe_url(username: str) -> str:
    return GoodreadsConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in GoodreadsConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, GoodreadsConstants.AVATAR_KEYS, GoodreadsConstants.COVER_KEYS)

ROUTES = (
    ("(?:user|author)/show/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("book/show/(?P<id>[^/]+)", "post"),
    ("group/show/(?P<id>[^/]+)", "group"),
    ("(?P<id>[^/]+)", "profile"),
)
