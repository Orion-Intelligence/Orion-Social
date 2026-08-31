import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import OnlyFansConstants

constants = OnlyFansConstants


def probe_url(username: str) -> str:
    return OnlyFansConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in OnlyFansConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, clean(parse.social_info(body))

def clean(info: dict) -> dict:
    description = (info.get("description") or "").strip()
    if len(description) < 3 or any(description.casefold().startswith(prefix) for prefix in OnlyFansConstants.GENERIC_DESCRIPTIONS):
        info.pop("description", None)
    return {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
