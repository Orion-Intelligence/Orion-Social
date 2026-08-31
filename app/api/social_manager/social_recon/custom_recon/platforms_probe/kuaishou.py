import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import KuaishouConstants

constants = KuaishouConstants


def probe_url(username: str) -> str:
    return KuaishouConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    matches = payload.get("matches") if isinstance(payload, dict) else None
    if not matches:
        return VerdictConstants.UNKNOWN, {}
    first = matches[0] if isinstance(matches[0], dict) else {}
    info = {
        "display_name": parse.text(first.get("title")),
        "description": parse.text(first.get("body")),
        "avatar": parse.text(first.get("image")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("profile/(?P<id>[^/]+)", "profile"),
    ("short-video/(?P<id>[^/]+)", "video"),
)
