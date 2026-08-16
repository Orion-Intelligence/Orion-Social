import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import LichessConstants

constants = LichessConstants


def probe_url(username: str) -> str:
    return LichessConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(((payload.get("profile") or {}).get("realName")) or payload.get("username")),
        "description": parse.text((payload.get("profile") or {}).get("bio")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text(payload.get("createdAt")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("@/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("team/(?P<id>[^/]+)(?:/.*)?", "group"),
)
