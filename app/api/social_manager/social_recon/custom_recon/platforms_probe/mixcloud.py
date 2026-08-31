import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import MixcloudConstants

constants = MixcloudConstants


def probe_url(username: str) -> str:
    return MixcloudConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("name")),
        "description": parse.text(payload.get("biog")),
        "avatar": parse.text(((payload.get("pictures") or {}).get("extra_large"))),
        "followers": parse.text(payload.get("follower_count")),
        "created_at": parse.text(payload.get("created_time")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?P<id>[^/]+)/[^/]+/?", "post"),
    ("(?P<id>[^/]+)", "profile"),
)
