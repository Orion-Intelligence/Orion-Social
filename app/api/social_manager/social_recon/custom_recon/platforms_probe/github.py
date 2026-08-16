import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GitHubConstants

constants = GitHubConstants


def probe_url(username: str) -> str:
    return GitHubConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or not payload.get("login"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("name")),
        "description": parse.text(payload.get("bio")),
        "avatar": parse.text(payload.get("avatar_url")),
        "id": parse.text(payload.get("id")),
        "followers": parse.text(payload.get("followers")),
        "public_repos": parse.text(payload.get("public_repos")),
        "created_at": parse.text(payload.get("created_at")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("orgs/(?P<id>[^/]+)(?:/.*)?", "page"),
    ("(?P<id>[^/]+)/(?P<repo>[^/]+)(?:/.*)?", "repo"),
    ("(?P<id>[^/]+)", "profile"),
)
