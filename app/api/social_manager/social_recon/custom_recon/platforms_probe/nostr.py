import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import NostrConstants

constants = NostrConstants


def probe_url(username: str) -> str:
    return NostrConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, clean(parse.social_info(body))


evaluate_resource = evaluate

def clean(info: dict) -> dict:
    description = (info.get("description") or "").strip()
    if len(description) < 3 or any(description.casefold().startswith(prefix) for prefix in NostrConstants.GENERIC_DESCRIPTIONS):
        info.pop("description", None)
    return {key: value for key, value in info.items() if value}

HOSTS = ("nostr.com", "primal.net", "snort.social")
ROUTES = (
    ("(?:e/)?(?P<id>note1[a-z0-9]+|nevent1[a-z0-9]+)", "post"),
    ("(?:p/)?(?P<id>npub1[a-z0-9]+|nprofile1[a-z0-9]+|[^/]+@[^/]+)", "profile"),
)
