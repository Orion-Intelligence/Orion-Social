import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import NotionConstants

constants = NotionConstants


def probe_url(username: str) -> str:
    return NotionConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    heading = parse.title(body)
    if not heading or heading.casefold() in NotionConstants.GENERIC:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, NotionConstants.AVATAR_KEYS, NotionConstants.COVER_KEYS)
    name = parse.clean(parse.text(info.get("display_name") or heading).split(" | ")[0])
    if name:
        info["display_name"] = name
    if info.get("description"):
        info["description"] = parse.clean(info["description"])
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

HOSTS = ("notion.site",)
ROUTES = (
    ("(?P<id>[^/]+-[a-f0-9]{32})$", "page"),
    ("@(?P<id>[^/]+)(?:/.*)?", "profile"),
)

