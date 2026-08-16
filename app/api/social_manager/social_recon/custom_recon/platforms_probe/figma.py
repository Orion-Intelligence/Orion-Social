import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import FigmaConstants

constants = FigmaConstants


def probe_url(username: str) -> str:
    return FigmaConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status not in (200, 202):
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body)

ROUTES = (
    ("@(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"community/(?:file|plugin|widget)/(?P<id>\d+)(?:/.*)?", "post"),
    ("(?:design|file|proto|board)/(?P<id>[^/]+)(?:/.*)?", "post"),
)
