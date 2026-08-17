import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import SpotifyConstants

constants = SpotifyConstants


def probe_url(username: str) -> str:
    return SpotifyConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in SpotifyConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, clean(parse.social_info(body))


evaluate_resource = evaluate

def clean(info: dict) -> dict:
    description = (info.get("description") or "").strip()
    if len(description) < 3 or any(description.casefold().startswith(prefix) for prefix in SpotifyConstants.GENERIC_DESCRIPTIONS):
        info.pop("description", None)
    return {key: value for key, value in info.items() if value}

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("artist/(?P<id>[^/]+)", "page"),
    ("(?:track|album|playlist|episode|show)/(?P<id>[^/]+)", "post"),
)
