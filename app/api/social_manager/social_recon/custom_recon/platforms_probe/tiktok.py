import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import TikTokConstants

constants = TikTokConstants


def probe_url(username: str) -> str:
    return TikTokConstants.OEMBED_URL.format(username=username)


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status in (400, 404):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    payload = parse.as_json(body)
    if not isinstance(payload, dict) or not payload.get("author_url"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.text(payload.get("author_name")),
        "avatar": parse.text(payload.get("thumbnail_url")),
        "title": parse.text(payload.get("title")),
        "image_note": "" if payload.get("thumbnail_url") else TikTokConstants.IMAGE_NOTE,
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
