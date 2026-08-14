import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BlueskyConstants

constants = BlueskyConstants


def handle(username: str) -> str:
    return username if "." in username else username + BlueskyConstants.DEFAULT_DOMAIN


def probe_url(username: str) -> str:
    return BlueskyConstants.API_URL.format(handle=handle(username))


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 400:
        payload = parse.as_json(body)
        message = parse.text((payload or {}).get("message")).casefold() if isinstance(payload, dict) else ""
        return (VerdictConstants.ABSENT, {}) if "not found" in message else (VerdictConstants.UNKNOWN, {})
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or not payload.get("did"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("displayName")),
        "description": parse.text(payload.get("description")),
        "avatar": parse.text(payload.get("avatar")),
        "cover": parse.text(payload.get("banner")),
        "id": parse.text(payload.get("did")),
        "handle": parse.text(payload.get("handle")),
        "followers": parse.text(payload.get("followersCount")),
        "following": parse.text(payload.get("followsCount")),
        "posts": parse.text(payload.get("postsCount")),
        "created_at": parse.text(payload.get("createdAt")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
