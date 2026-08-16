import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import KeybaseConstants

constants = KeybaseConstants


def probe_url(username: str) -> str:
    return KeybaseConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and ((payload.get("status") or {}).get("code") not in (0, None) or (isinstance(payload.get("them"), list) and payload["them"] and payload["them"][0] is None)):
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and isinstance(payload.get("them"), list) and payload["them"] and payload["them"][0]):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(((payload["them"][0].get("profile") or {}).get("full_name"))),
        "description": parse.text(((payload["them"][0].get("profile") or {}).get("bio"))),
        "avatar": parse.text((((payload["them"][0].get("pictures") or {}).get("primary") or {}).get("url"))),
        "id": parse.text(payload["them"][0].get("id")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
