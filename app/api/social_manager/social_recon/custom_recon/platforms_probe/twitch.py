import json

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import TwitchConstants

constants = TwitchConstants


def probe_url(username: str) -> str:
    return TwitchConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    payload = json.dumps({"query": TwitchConstants.GQL_QUERY.format(username=username)})
    headers = {"Client-Id": TwitchConstants.GQL_CLIENT_ID, "Content-Type": "application/json"}
    return http_client.post(TwitchConstants.GQL_URL, payload, headers)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or "data" not in payload:
        return VerdictConstants.UNKNOWN, {}
    user = (payload.get("data") or {}).get("user")
    if user is None:
        return VerdictConstants.ABSENT, {}
    if not isinstance(user, dict) or not user.get("id"):
        return VerdictConstants.UNKNOWN, {}
    followers = user.get("followers") or {}
    info = {
        "display_name": parse.text(user.get("displayName")),
        "description": parse.text(user.get("description")),
        "avatar": parse.text(user.get("profileImageURL")),
        "cover": parse.text(user.get("bannerImageURL") or user.get("offlineImageURL")),
        "id": parse.text(user.get("id")),
        "followers": parse.text(followers.get("totalCount") if isinstance(followers, dict) else None),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
