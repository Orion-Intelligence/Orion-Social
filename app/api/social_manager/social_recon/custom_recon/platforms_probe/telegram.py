import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import TelegramConstants

constants = TelegramConstants


def probe_url(username: str) -> str:
    return TelegramConstants.PROFILE_URL.format(username=username)


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

HOSTS = ("telegram.me",)
ROUTES = (
    ("s/(?P<id>[^/]+)(?:/.*)?", "channel"),
    (r"(?:joinchat/|\+)(?P<id>[^/]+)", "group"),
    ("(?P<id>[^/]+)", "profile"),
)

