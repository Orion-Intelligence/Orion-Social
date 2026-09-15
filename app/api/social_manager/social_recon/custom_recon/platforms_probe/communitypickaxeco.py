import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import CommunityPickaxeCoConstants

constants = CommunityPickaxeCoConstants


def probe_url(username: str) -> str:
    return CommunityPickaxeCoConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    user = payload.get("user") if isinstance(payload, dict) else None
    if not isinstance(user, dict) or not user.get("username"):
        return VerdictConstants.UNKNOWN, {}
    base = CommunityPickaxeCoConstants.PROFILE_URL.split("/u/")[0]
    avatar = parse.text(user.get("avatar_template"))
    if avatar.startswith("/"):
        avatar = f"{base}{avatar}".replace("{size}", "240")
    info = {
        "display_name": parse.clean(user.get("name")),
        "username": parse.text(user.get("username")),
        "description": parse.clean(user.get("bio_raw") or user.get("bio_excerpt")),
        "avatar": "" if parse.is_generic_image(avatar) else avatar,
        "location": parse.clean(user.get("location")),
        "website": parse.text(user.get("website_name") or user.get("website")),
        "id": parse.text(user.get("id")),
        "created_at": parse.text(user.get("created_at")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


ROUTES = (
    (r"u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
