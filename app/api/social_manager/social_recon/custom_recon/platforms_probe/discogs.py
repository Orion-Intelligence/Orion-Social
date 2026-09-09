import re

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import DiscogsConstants

constants = DiscogsConstants


def probe_url(username: str) -> str:
    return DiscogsConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    return http_client.fetch(DiscogsConstants.API_URL.format(username=username))


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    data = parse.as_json(body)
    if not (isinstance(data, dict) and data.get("username")):
        return VerdictConstants.UNKNOWN, {}
    avatar = parse.text(data.get("avatar_url"))
    info = {
        "display_name": parse.clean(data.get("name") or data.get("username")),
        "username": parse.text(data.get("username")),
        "description": parse.clean(data.get("profile")),
        "avatar": "" if parse.is_generic_image(avatar) else avatar,
        "cover": parse.text(data.get("banner_url")),
        "id": parse.text(data.get("id")),
        "location": parse.clean(data.get("location")),
        "website": parse.text(data.get("home_page")),
        "created_at": parse.text(data.get("registered")),
        "collection": parse.text(data.get("num_collection")) if data.get("num_collection") else "",
        "wantlist": parse.text(data.get("num_wantlist")) if data.get("num_wantlist") else "",
        "lists": parse.text(data.get("num_lists")) if data.get("num_lists") else "",
        "contributions": parse.text(data.get("releases_contributed")) if data.get("releases_contributed") else "",
        "rank": parse.text(data.get("rank")) if data.get("rank") else "",
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    artist = re.search(r"/artist/(\d+)", final_url or "")
    if artist:
        code, payload, _ = http_client.fetch(DiscogsConstants.ARTIST_API.format(id=artist.group(1)))
        if code == 404:
            return VerdictConstants.ABSENT, {}
        data = parse.as_json(payload) if code == 200 else None
        if isinstance(data, dict) and data.get("name"):
            images = data.get("images") if isinstance(data.get("images"), list) else []
            urls = data.get("urls") if isinstance(data.get("urls"), list) else []
            info = {
                "title": parse.clean(data.get("name")),
                "description": parse.clean(data.get("profile")),
                "image": parse.text(images[0].get("uri")) if images and isinstance(images[0], dict) else "",
                "id": parse.text(data.get("id")),
            }
            for name, link in parse.social_links(urls).items():
                info.setdefault(name, link)
            return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    meta = parse.meta(body)
    info = {"title": parse.clean(meta.get("og:title") or parse.title(body)), "description": parse.clean(meta.get("og:description")), "image": parse.text(meta.get("og:image"))}
    return (VerdictConstants.EXISTS, {k: v for k, v in info.items() if v}) if any(info.values()) else (VerdictConstants.UNKNOWN, {})

ROUTES = (
    (r"artist/(?P<id>\d+)(?:.*)?", "page"),
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
