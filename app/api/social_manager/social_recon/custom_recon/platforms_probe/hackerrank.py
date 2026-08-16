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
    info = {
        "display_name": parse.text(payload["model"].get("name")),
        "avatar": parse.text(payload["model"].get("avatar")),
        "id": parse.text(payload["model"].get("id")),
        "country": parse.text(payload["model"].get("country")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?:profile/)?(?P<id>[^/]+)", "profile"),
)
