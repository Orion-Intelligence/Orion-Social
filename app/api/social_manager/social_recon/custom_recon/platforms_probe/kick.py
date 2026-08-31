import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import KickConstants

constants = KickConstants


def probe_url(username: str) -> str:
    return KickConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or not payload.get("id"):
        return VerdictConstants.UNKNOWN, {}
    user = payload.get("user") if isinstance(payload.get("user"), dict) else {}
    info = {
        "display_name": parse.text(user.get("username")),
        "description": parse.text(user.get("bio")),
        "avatar": parse.text(user.get("profile_pic")),
        "cover": parse.text((payload.get("banner_image") or {}).get("url") if isinstance(payload.get("banner_image"), dict) else None),
        "id": parse.text(payload.get("id")),
        "followers": parse.text(payload.get("followers_count")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("video/(?P<id>[^/]+)", "video"),
    ("(?P<id>[^/]+)/videos/(?P<video>[^/]+)", "video"),
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
