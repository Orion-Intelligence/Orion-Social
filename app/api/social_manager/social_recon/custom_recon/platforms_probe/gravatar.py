import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import GravatarConstants

constants = GravatarConstants


def probe_url(username: str) -> str:
    return GravatarConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not (isinstance(payload, dict) and isinstance(payload.get("entry"), list) and payload["entry"]):
        return VerdictConstants.UNKNOWN, {}
    entry = payload["entry"][0] if isinstance(payload["entry"][0], dict) else {}
    background = entry.get("profileBackground") if isinstance(entry.get("profileBackground"), dict) else {}
    info = {
        "display_name": parse.clean(entry.get("displayName")),
        "username": parse.text(entry.get("preferredUsername")),
        "description": parse.clean(entry.get("aboutMe")),
        "avatar": parse.text(entry.get("thumbnailUrl")),
        "cover": parse.text(background.get("url")),
        "id": parse.text(entry.get("id")),
        "location": parse.clean(entry.get("currentLocation")),
        "job": parse.clean(entry.get("job_title")),
        "company": parse.clean(entry.get("company")),
        "pronouns": parse.clean(entry.get("pronouns")),
    }
    for account in entry.get("accounts") or []:
        if not isinstance(account, dict) or not account.get("url"):
            continue
        key = parse.clean(account.get("shortname") or account.get("name")).lower()
        if key and not info.get(key):
            info[key] = parse.text(account.get("url"))
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

HOSTS = ("en.gravatar.com",)
ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
