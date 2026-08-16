import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import Lemon8Constants

constants = Lemon8Constants


def probe_url(username: str) -> str:
    return Lemon8Constants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, Lemon8Constants.AVATAR_KEYS, Lemon8Constants.COVER_KEYS)

ROUTES = (
    (r"@(?P<id>[^/]+)/(?P<post>\d+)(?:/.*)?", "post"),
    ("@(?P<id>[^/]+)", "profile"),
)
