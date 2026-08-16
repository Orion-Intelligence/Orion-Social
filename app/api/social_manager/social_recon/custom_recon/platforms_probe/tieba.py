import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import BaiduTiebaConstants

constants = BaiduTiebaConstants


def probe_url(username: str) -> str:
    return BaiduTiebaConstants.PANEL_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or "no" not in payload:
        return VerdictConstants.UNKNOWN, {}
    if payload.get("no") != 0:
        return VerdictConstants.ABSENT, {}
    data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
    info = {
        "display_name": parse.text(data.get("name_show") or data.get("name")),
        "avatar": parse.text(data.get("portrait")),
        "id": parse.text(data.get("id")),
        "followers": parse.text(data.get("followed_count")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    (r"home/main\?(?:.*&)?un=(?P<id>[^&]+)(?:&.*)?", "profile"),
    (r"f\?(?:.*&)?kw=(?P<id>[^&]+)(?:&.*)?", "group"),
    (r"p/(?P<id>\d+)", "post"),
)
