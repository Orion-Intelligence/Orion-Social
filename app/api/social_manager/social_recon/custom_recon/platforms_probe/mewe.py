import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import MeWeConstants

constants = MeWeConstants


def probe_url(username: str) -> str:
    return MeWeConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, final_url: str) -> tuple[str, dict]:
    if status == 404 or (final_url or "").rstrip("/").endswith(MeWeConstants.NOT_FOUND_PATH):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in MeWeConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body)

ROUTES = (
    ("i/(?P<id>[^/]+)", "profile"),
    ("(?:join|group)/(?P<id>[^/]+)", "group"),
    ("p/(?P<id>[^/]+)", "page"),
)
