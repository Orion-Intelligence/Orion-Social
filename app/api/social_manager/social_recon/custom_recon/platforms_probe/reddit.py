import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import RedditConstants

constants = RedditConstants


def probe_url(username: str) -> str:
    return RedditConstants.ABOUT_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status == 404:
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict):
        return VerdictConstants.UNKNOWN, {}
    data = payload.get("data")
    if not isinstance(data, dict) or not data.get("name"):
        return VerdictConstants.UNKNOWN, {}
    profile = data.get("subreddit") if isinstance(data.get("subreddit"), dict) else {}
    info = {
        "display_name": parse.text(data.get("name")),
        "avatar": parse.text(data.get("icon_img") or profile.get("icon_img")).split("?")[0],
        "cover": parse.text(profile.get("banner_img")).split("?")[0],
        "id": parse.text(data.get("id")),
        "total_karma": parse.text(data.get("total_karma")),
        "created_utc": parse.text(data.get("created_utc")),
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
