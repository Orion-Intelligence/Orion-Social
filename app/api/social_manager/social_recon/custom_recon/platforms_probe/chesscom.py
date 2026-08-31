import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import ChessComConstants

constants = ChessComConstants


def probe_url(username: str) -> str:
    return ChessComConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("name") or payload.get("username")),
        "avatar": parse.text(payload.get("avatar")),
        "id": parse.text(payload.get("player_id")),
        "followers": parse.text(payload.get("followers")),
        "created_at": parse.text(payload.get("joined")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("member/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("club/(?P<id>[^/]+)(?:/.*)?", "group"),
)
