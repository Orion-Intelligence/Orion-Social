import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import WikipediaConstants

constants = WikipediaConstants


def probe_url(username: str) -> str:
    return WikipediaConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    users = ((payload.get("query") or {}).get("users")) if isinstance(payload, dict) else None
    if isinstance(users, list) and users and ("missing" in users[0] or "invalid" in users[0]):
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and isinstance(((payload.get("query") or {}).get("users")), list) and payload["query"]["users"] and payload["query"]["users"][0].get("userid")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload["query"]["users"][0].get("name")),
        "id": parse.text(payload["query"]["users"][0].get("userid")),
        "created_at": parse.text(payload["query"]["users"][0].get("registration")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("wiki/User:(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("wiki/(?P<id>[^/]+)", "page"),
)
