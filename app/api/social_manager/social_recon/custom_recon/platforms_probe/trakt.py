import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import TraktConstants

constants = TraktConstants


def probe_url(username: str) -> str:
    return TraktConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body).casefold()
    if heading == TraktConstants.NOT_FOUND_TITLE:
        return VerdictConstants.ABSENT, {}
    if not heading or heading in TraktConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, clean(parse.social_info(body))


evaluate_resource = evaluate

def clean(info: dict) -> dict:
    description = (info.get("description") or "").strip()
    if len(description) < 3 or any(description.casefold().startswith(prefix) for prefix in TraktConstants.GENERIC_DESCRIPTIONS):
        info.pop("description", None)
    return {key: value for key, value in info.items() if value}

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("(?:movies|shows)/(?P<id>[^/]+)(?:/.*)?", "post"),
)
