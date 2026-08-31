import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import VimeoConstants

constants = VimeoConstants


def probe_url(username: str) -> str:
    return VimeoConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("id")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("display_name")),
        "description": parse.text(payload.get("bio")),
        "avatar": parse.text(payload.get("portrait_huge") or payload.get("portrait_large")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text(payload.get("created_on")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    (r"(?P<id>\d+)", "video"),
    ("(?P<id>[^/]+)", "profile"),
)
