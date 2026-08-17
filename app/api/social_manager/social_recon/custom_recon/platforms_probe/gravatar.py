import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GravatarConstants

constants = GravatarConstants


def probe_url(username: str) -> str:
    return GravatarConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and isinstance(payload.get("entry"), list) and payload["entry"]):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload["entry"][0].get("displayName")),
        "description": parse.text(payload["entry"][0].get("aboutMe")),
        "avatar": parse.text(payload["entry"][0].get("thumbnailUrl")),
        "id": parse.text(payload["entry"][0].get("id")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

HOSTS = ("en.gravatar.com",)
ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
