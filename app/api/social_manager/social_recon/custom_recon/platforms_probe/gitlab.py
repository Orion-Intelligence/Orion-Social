import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GitLabConstants

constants = GitLabConstants


def probe_url(username: str) -> str:
    return GitLabConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, list):
        return VerdictConstants.UNKNOWN, {}
    if not payload:
        return VerdictConstants.ABSENT, {}
    user = payload[0] if isinstance(payload[0], dict) else {}
    if not user.get("username"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(user.get("name")),
        "avatar": parse.text(user.get("avatar_url")),
        "id": parse.text(user.get("id")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("groups/(?P<id>[^/]+)(?:/.*)?", "group"),
    ("(?P<id>[^/]+)/(?P<repo>[^/]+)(?:/.*)?", "repo"),
    ("(?P<id>[^/]+)", "profile"),
)
