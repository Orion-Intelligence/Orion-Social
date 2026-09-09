import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import SpeedrunComConstants

constants = SpeedrunComConstants


def probe_url(username: str) -> str:
    return SpeedrunComConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and isinstance(payload.get("data"), dict) and payload["data"].get("id")):
        return VerdictConstants.UNKNOWN, {}
    data = payload["data"]
    name = parse.text((data.get("names") or {}).get("international"))
    country = (((data.get("location") or {}).get("country") or {}).get("names") or {}).get("international") if isinstance(data.get("location"), dict) else None

    def link(key: str) -> str:
        value = data.get(key)
        return parse.text(value.get("uri")) if isinstance(value, dict) else ""

    info = {
        "display_name": name,
        "username": name,
        "id": parse.text(data.get("id")),
        "created_at": parse.text(data.get("signup")),
        "location": parse.clean(country),
        "twitch": link("twitch"),
        "youtube": link("youtube"),
        "twitter": link("twitter"),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("users?/(?P<id>[^/]+)(?:/.*)?", "profile"),
)



