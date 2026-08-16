import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import MediumConstants

constants = MediumConstants


def probe_url(username: str) -> str:
    return MediumConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json((body or "").removeprefix(MediumConstants.JSON_PREFIX))
    if not isinstance(payload, dict) or "success" not in payload:
        return VerdictConstants.UNKNOWN, {}
    user = ((payload.get("payload") or {}).get("user") or {}) if payload.get("success") else {}
    if not user or not user.get("username"):
        return VerdictConstants.ABSENT, {}
    info = {
        "display_name": parse.text(user.get("name")),
        "description": parse.text(user.get("bio")),
        "avatar": f"https://miro.medium.com/{user.get('imageId')}" if user.get("imageId") else "",
        "id": parse.text(user.get("userId")),
        "created_at": parse.text(user.get("createdAt")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

SUBDOMAIN = ("medium.com", "page")
ROUTES = (
    ("@(?P<id>[^/@]+)/(?P<post>[^/]+)", "post"),
    ("@(?P<id>[^/@]+)", "profile"),
    ("(?P<id>[^/@]+)/(?P<post>[^/]+)", "post"),
    ("(?P<id>[^/@]+)", "page"),
)
