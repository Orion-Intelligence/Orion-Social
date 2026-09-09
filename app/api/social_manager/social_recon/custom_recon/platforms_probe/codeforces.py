import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import CodeforcesConstants

constants = CodeforcesConstants


def probe_url(username: str) -> str:
    return CodeforcesConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    payload = parse.as_json(body)
    if status in (400, 404) or (isinstance(payload, dict) and payload.get("status") == "FAILED"):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    if not (isinstance(payload, dict) and payload.get("status") == "OK" and payload.get("result")):
        return VerdictConstants.UNKNOWN, {}
    user = payload["result"][0] if isinstance(payload["result"][0], dict) else {}
    name = parse.clean(" ".join(filter(None, (user.get("firstName"), user.get("lastName")))))
    location = ", ".join(filter(None, (parse.clean(user.get("city")), parse.clean(user.get("country")))))
    info = {
        "display_name": name or parse.text(user.get("handle")),
        "username": parse.text(user.get("handle")),
        "avatar": parse.text(user.get("titlePhoto") or user.get("avatar")),
        "location": location,
        "organization": parse.clean(user.get("organization")),
        "rank": parse.text(user.get("rank")),
        "max_rank": parse.text(user.get("maxRank")),
        "rating": parse.text(user.get("rating")) if user.get("rating") else "",
        "max_rating": parse.text(user.get("maxRating")) if user.get("maxRating") else "",
        "contribution": parse.text(user.get("contribution")) if user.get("contribution") else "",
        "followers": parse.text(user.get("friendOfCount")) if user.get("friendOfCount") else "",
        "created_at": parse.text(user.get("registrationTimeSeconds")),
        "last_online": parse.text(user.get("lastOnlineTimeSeconds")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    (r"contest/(?P<id>\d+)(?:/.*)?", "page"),
    ("group/(?P<id>[^/]+)(?:/.*)?", "group"),
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)


