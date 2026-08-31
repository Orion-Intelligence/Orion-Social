import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import CratesIoConstants

constants = CratesIoConstants


def probe_url(username: str) -> str:
    return CratesIoConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and isinstance(payload.get("user"), dict) and payload["user"].get("login")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload["user"].get("name") or payload["user"].get("login")),
        "avatar": parse.text(payload["user"].get("avatar")),
        "id": parse.text(payload["user"].get("id")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("crates/(?P<id>[^/]+)(?:/.*)?", "repo"),
)
