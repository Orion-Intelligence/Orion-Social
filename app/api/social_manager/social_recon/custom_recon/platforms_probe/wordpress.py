import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import WordPressComConstants

constants = WordPressComConstants


def probe_url(username: str) -> str:
    return WordPressComConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("ID")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("name")),
        "description": parse.text(payload.get("description")),
        "avatar": parse.text((payload.get("icon") or {}).get("img") if isinstance(payload.get("icon"), dict) else None),
        "id": parse.text(payload.get("ID")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

HOSTS = ("wordpress.com",)
SUBDOMAIN = ("wordpress.com", "profile")
ROUTES = (
    ("(?P<id>[a-z0-9.-]+)", "profile"),
)
