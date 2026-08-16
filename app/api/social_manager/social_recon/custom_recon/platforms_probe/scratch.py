import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import ScratchConstants

constants = ScratchConstants


def probe_url(username: str) -> str:
    return ScratchConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("username")),
        "description": parse.text((payload.get("profile") or {}).get("bio")),
        "avatar": parse.text((((payload.get("profile") or {}).get("images")) or {}).get("90x90")),
        "id": parse.text(payload.get("id")),
        "created_at": parse.text((payload.get("history") or {}).get("joined")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"projects/(?P<id>\d+)(?:/.*)?", "post"),
    (r"studios/(?P<id>\d+)(?:/.*)?", "group"),
)
