import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import LiveJournalConstants

constants = LiveJournalConstants


def probe_url(username: str) -> str:
    return LiveJournalConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in LiveJournalConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, parse.social_info(body, LiveJournalConstants.AVATAR_KEYS, LiveJournalConstants.COVER_KEYS)

HOSTS = ("livejournal.com",)
SUBDOMAIN = ("livejournal.com", "profile")
ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("community/(?P<id>[^/]+)(?:/.*)?", "group"),
)
