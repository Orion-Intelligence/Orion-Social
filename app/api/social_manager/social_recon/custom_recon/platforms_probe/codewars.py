import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import CodewarsConstants

constants = CodewarsConstants


def probe_url(username: str) -> str:
    return CodewarsConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and payload.get("username")):
        return VerdictConstants.UNKNOWN, {}
    ranks = payload.get("ranks") if isinstance(payload.get("ranks"), dict) else {}
    overall = ranks.get("overall") if isinstance(ranks.get("overall"), dict) else {}
    skills = payload.get("skills") if isinstance(payload.get("skills"), list) else []
    info = {
        "display_name": parse.clean(payload.get("name") or payload.get("username")),
        "username": parse.text(payload.get("username")),
        "id": parse.text(payload.get("id")),
        "clan": parse.clean(payload.get("clan")),
        "honor": parse.text(payload.get("honor")) if payload.get("honor") else "",
        "leaderboard_position": parse.text(payload.get("leaderboardPosition")) if payload.get("leaderboardPosition") else "",
        "rank": parse.text(overall.get("name")),
        "skills": ", ".join(parse.clean(skill) for skill in skills if skill),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)


