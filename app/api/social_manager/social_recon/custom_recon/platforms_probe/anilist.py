import json

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import AniListConstants

constants = AniListConstants


def probe_url(username: str) -> str:
    return AniListConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    payload = json.dumps({"query": AniListConstants.GQL_QUERY, "variables": {"name": username}})
    return http_client.post(AniListConstants.GQL_URL, payload, {"Content-Type": "application/json", "Accept": "application/json"})


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    user = (payload.get("data") or {}).get("User") if isinstance(payload, dict) else None
    if not isinstance(user, dict) or not user.get("id"):
        return VerdictConstants.UNKNOWN, {}
    avatar = user.get("avatar") if isinstance(user.get("avatar"), dict) else {}
    info = {
        "display_name": parse.text(user.get("name")),
        "description": parse.text(user.get("about")),
        "avatar": parse.text(avatar.get("large")),
        "cover": parse.text(user.get("bannerImage")),
        "id": parse.text(user.get("id")),
        "created_at": parse.text(user.get("createdAt")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"(?:anime|manga)/(?P<id>\d+)(?:/.*)?", "post"),
    (r"activity/(?P<id>\d+)", "post"),
)
