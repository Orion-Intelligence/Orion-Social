from urllib.parse import urlparse

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BitChuteConstants

constants = BitChuteConstants


def probe_url(username: str) -> str:
    return BitChuteConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, final_url: str) -> tuple[str, dict]:
    if status == 404 or urlparse(final_url or "").path.strip("/") == "":
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body)

ROUTES = (
    ("channel/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("video/(?P<id>[^/]+)(?:/.*)?", "video"),
)
