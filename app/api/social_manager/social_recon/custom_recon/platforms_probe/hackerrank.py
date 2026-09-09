import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import HackerRankConstants

constants = HackerRankConstants


def probe_url(username: str) -> str:
    return HackerRankConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and isinstance(payload.get("model"), dict) and payload["model"].get("username")):
        return VerdictConstants.UNKNOWN, {}
    model = payload["model"]
    avatar = parse.text(model.get("avatar"))
    info = {
        "display_name": parse.clean(model.get("name")),
        "username": parse.text(model.get("username")),
        "description": parse.clean(model.get("short_bio")),
        "avatar": "" if parse.is_generic_image(avatar) else avatar,
        "id": parse.text(model.get("id")),
        "location": parse.clean(model.get("country")),
        "school": parse.clean(model.get("school")),
        "level": parse.text(model.get("level")) if model.get("level") else "",
        "website": parse.text(model.get("website")),
        "created_at": parse.text(model.get("created_at")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?:profile/)?(?P<id>[^/]+)", "profile"),
)


