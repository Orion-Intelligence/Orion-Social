import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import ThreadsConstants

constants = ThreadsConstants


def probe_url(username: str) -> str:
    return ThreadsConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body).casefold()
    if not heading or ThreadsConstants.LOGIN_MARKER in heading:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, ThreadsConstants.AVATAR_KEYS, ThreadsConstants.COVER_KEYS)
    counts = parse.counts(info.get("description", ""))
    info.update({key: counts[key] for key in ("followers", "following", "posts") if key in counts})
    if "threads" in counts:
        info.setdefault("posts", counts["threads"])
    return VerdictConstants.EXISTS, info

HOSTS = ("threads.com",)
ROUTES = (
    (r"@?(?P<id>[^/@]+)/post/[^/]+", "post"),
    (r"@?(?P<id>[^/@]+)", "profile"),
)
