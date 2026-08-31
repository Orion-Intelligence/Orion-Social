import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import DailymotionConstants

constants = DailymotionConstants


def probe_url(username: str) -> str:
    return DailymotionConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("id")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("screenname")),
        "description": parse.text(payload.get("description")),
        "avatar": parse.text(payload.get("avatar_360_url")),
        "id": parse.text(payload.get("id")),
        "followers": parse.text(payload.get("followers_total")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("video/(?P<id>[^/]+)", "video"),
    ("(?P<id>[^/]+)", "profile"),
)
