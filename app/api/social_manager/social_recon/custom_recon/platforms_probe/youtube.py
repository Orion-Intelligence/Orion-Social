import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import YouTubeConstants

constants = YouTubeConstants


def probe_url(username: str) -> str:
    return YouTubeConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, YouTubeConstants.AVATAR_KEYS, YouTubeConstants.COVER_KEYS, cover_pattern=YouTubeConstants.COVER_PATTERN)

HOSTS = ("youtu.be",)
ROUTES = (
    (r"@(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"channel/(?P<id>UC[\w-]+)(?:/.*)?", "channel"),
    (r"(?:shorts/)?(?P<id>[\w-]{11})", "video"),
    (r"watch\?(?:.*&)?v=(?P<id>[\w-]+)(?:&.*)?", "video"),
)
