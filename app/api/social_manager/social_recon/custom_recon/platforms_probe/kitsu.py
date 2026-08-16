import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import KitsuConstants

constants = KitsuConstants


def probe_url(username: str) -> str:
    return KitsuConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and isinstance(payload.get("data"), list) and not payload["data"]:
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and isinstance(payload.get("data"), list) and payload["data"] and isinstance(payload["data"][0], dict)):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(((payload["data"][0].get("attributes") or {}).get("name"))),
        "description": parse.text(((payload["data"][0].get("attributes") or {}).get("about"))),
        "avatar": parse.text(((((payload["data"][0].get("attributes") or {}).get("avatar")) or {}).get("original"))),
        "id": parse.text(payload["data"][0].get("id")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

HOSTS = ("kitsu.app",)
ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("(?:anime|manga)/(?P<id>[^/]+)(?:/.*)?", "post"),
)
