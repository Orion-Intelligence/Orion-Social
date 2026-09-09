import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import AboutMeConstants

constants = AboutMeConstants


def probe_url(username: str) -> str:
    return AboutMeConstants.PROFILE_URL.format(username=username)


def _first(items: object, key: str) -> str:
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get(key):
                return parse.text(item[key])
    return ""


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    profile = parse.embedded_object(body, AboutMeConstants.DATA_KEY)
    if not (isinstance(profile, dict) and profile.get("user_name")):
        heading = parse.title(body)
        if not heading or heading.casefold() in AboutMeConstants.GENERIC:
            return VerdictConstants.UNKNOWN, {}
        return VerdictConstants.EXISTS, parse.social_info(body, AboutMeConstants.AVATAR_KEYS, AboutMeConstants.COVER_KEYS)
    images = profile.get("images") if isinstance(profile.get("images"), list) else []
    image = images[0] if images and isinstance(images[0], dict) else {}
    name = parse.clean(f"{parse.text(profile.get('first_name'))} {parse.text(profile.get('last_name'))}")
    info = {
        "display_name": name,
        "username": parse.text(profile.get("user_name")),
        "description": parse.clean(profile.get("bio")),
        "cover": parse.text(image.get("url") or image.get("thumbnail_url")),
        "location": _first(profile.get("locations"), "location"),
        "company": _first(profile.get("jobs"), "job"),
        "id": parse.text(profile.get("user_id")),
        "twitter": parse.text(profile.get("twitter_username")),
    }
    for app in profile.get("apps") or []:
        if not isinstance(app, dict):
            continue
        platform, site = parse.text(app.get("platform")).lower(), parse.text(app.get("site_url"))
        if platform in AboutMeConstants.LINK_PLATFORMS and site and not info.get(platform):
            info[platform] = site
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
