import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import KeybaseConstants

constants = KeybaseConstants


def probe_url(username: str) -> str:
    return KeybaseConstants.API_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and ((payload.get("status") or {}).get("code") not in (0, None) or (isinstance(payload.get("them"), list) and payload["them"] and payload["them"][0] is None)):
        return VerdictConstants.ABSENT, {}
    if not (isinstance(payload, dict) and isinstance(payload.get("them"), list) and payload["them"] and payload["them"][0]):
        return VerdictConstants.UNKNOWN, {}
    them = payload["them"][0]
    profile = them.get("profile") if isinstance(them.get("profile"), dict) else {}
    basics = them.get("basics") if isinstance(them.get("basics"), dict) else {}
    pictures = them.get("pictures") if isinstance(them.get("pictures"), dict) else {}
    proofs = (them.get("proofs_summary") or {}).get("by_presentation_group") if isinstance(them.get("proofs_summary"), dict) else {}
    info = {
        "display_name": parse.clean(profile.get("full_name")),
        "username": parse.text(basics.get("username")),
        "description": parse.clean(profile.get("bio")),
        "avatar": parse.text((pictures.get("primary") or {}).get("url")),
        "location": parse.clean(profile.get("location")),
        "id": parse.text(them.get("id")),
        "created_at": parse.text(basics.get("ctime")),
    }
    for service, entries in (proofs or {}).items():
        if isinstance(entries, list) and entries and isinstance(entries[0], dict):
            link = parse.text(entries[0].get("service_url") or entries[0].get("nametag"))
            key = parse.text(service).lower()
            if key.startswith(("web", "dns", "http")):
                key = "website"
            if link and key and not info.get(key):
                info[key] = link
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
