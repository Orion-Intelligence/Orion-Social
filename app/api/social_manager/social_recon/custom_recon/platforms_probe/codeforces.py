import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import CodeforcesConstants

constants = CodeforcesConstants


def probe_url(username: str) -> str:
    return CodeforcesConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if status == 400 or (isinstance(payload, dict) and payload.get("status") == "FAILED"):
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and payload.get("status") == "OK" and payload.get("result")):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(" ".join(filter(None, (payload["result"][0].get("firstName"), payload["result"][0].get("lastName"))))),
        "avatar": parse.text(payload["result"][0].get("titlePhoto")),
        "rating": parse.text(payload["result"][0].get("rating")),
        "rank": parse.text(payload["result"][0].get("rank")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
