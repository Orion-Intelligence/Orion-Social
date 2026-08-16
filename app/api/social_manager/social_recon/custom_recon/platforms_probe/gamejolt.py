import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GameJoltConstants

constants = GameJoltConstants


def probe_url(username: str) -> str:
    return GameJoltConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or "payload" not in payload:
        return VerdictConstants.UNKNOWN, {}
    user = (payload.get("payload") or {}).get("user") if isinstance(payload.get("payload"), dict) else None
    if not isinstance(user, dict) or not user.get("username"):
        return VerdictConstants.ABSENT, {}
    info = {
        "display_name": parse.text(user.get("display_name") or user.get("name")),
        "avatar": parse.text(user.get("img_avatar")),
        "id": parse.text(user.get("id")),
        "followers": parse.text(user.get("follower_count")),
        "website": parse.text(user.get("web_site")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("@(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"games/(?P<id>[^/]+)/(?P<game>\d+)(?:/.*)?", "post"),
    ("c/(?P<id>[^/]+)(?:/.*)?", "group"),
)
