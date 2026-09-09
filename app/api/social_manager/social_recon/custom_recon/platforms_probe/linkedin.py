import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import LinkedInConstants

constants = LinkedInConstants


def probe_url(username: str) -> str:
    return LinkedInConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    info = parse.search_result(body)
    return (VerdictConstants.EXISTS, info) if info else (VerdictConstants.UNKNOWN, {})


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    info = parse.search_result(body)
    return (VerdictConstants.EXISTS, info) if info else (VerdictConstants.UNKNOWN, {})

ROUTES = (
    ("in/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("company/(?P<id>[^/]+)(?:/.*)?", "page"),
    (r"groups/(?P<id>\d+)(?:/.*)?", "group"),
)

