import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import InstagramConstants

constants = InstagramConstants


def probe_url(username: str) -> str:
    return InstagramConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in InstagramConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, InstagramConstants.AVATAR_KEYS, InstagramConstants.COVER_KEYS)
    info.update(parse.counts(info.get("description", "")))
    return VerdictConstants.EXISTS, info
