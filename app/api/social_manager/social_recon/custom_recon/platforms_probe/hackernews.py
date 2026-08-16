import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import HackerNewsConstants

constants = HackerNewsConstants


def probe_url(username: str) -> str:
    return HackerNewsConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if payload is None:
        return VerdictConstants.ABSENT, {}
    if not isinstance(payload, dict) or not payload.get("id"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "id": parse.text(payload.get("id")),
        "description": parse.text(payload.get("about")),
        "karma": parse.text(payload.get("karma")),
        "created_at": parse.text(payload.get("created")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    (r"user\?(?:.*&)?id=(?P<id>[^&]+)(?:&.*)?", "profile"),
    (r"item\?(?:.*&)?id=(?P<id>\d+)(?:&.*)?", "post"),
)
