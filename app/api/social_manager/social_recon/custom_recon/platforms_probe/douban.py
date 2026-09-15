import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import DoubanConstants

constants = DoubanConstants


def probe_url(username: str) -> str:
    return DoubanConstants.PROFILE_URL.format(username=username)


def evaluate(status: int, body: str, final_url: str) -> tuple[str, dict]:
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    absence = getattr(DoubanConstants, "ABSENCE", ())
    if absence and any(marker in body for marker in absence):
        return VerdictConstants.ABSENT, {}
    presence = getattr(DoubanConstants, "PRESENCE", ())
    if presence:
        if not any(marker in body for marker in presence):
            return VerdictConstants.UNKNOWN, {}
    elif status != 200:
        return VerdictConstants.UNKNOWN, {}
    info = parse.social_info(body, getattr(DoubanConstants, "AVATAR_KEYS", ()), getattr(DoubanConstants, "COVER_KEYS", ()))
    person = parse.ld_entity(body, "Person", "ProfilePage")
    if not info.get("display_name") and person.get("name"):
        info["display_name"] = person.get("name")
    if not info.get("description") and person.get("description"):
        info["description"] = person.get("description")
    if not info.get("avatar") and person.get("image"):
        candidate = parse.text(person.get("image"))
        info["avatar"] = "" if parse.is_generic_image(candidate) else candidate
    if info.get("display_name"):
        info["display_name"] = parse.clean(info["display_name"])
    if info.get("description"):
        info["description"] = parse.clean(info["description"])
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    (r"people/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
