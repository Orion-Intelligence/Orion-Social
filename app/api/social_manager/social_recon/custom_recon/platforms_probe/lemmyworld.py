import re

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import LemmyWorldConstants

constants = LemmyWorldConstants


def probe_url(username: str) -> str:
    return LemmyWorldConstants.PROFILE_URL.format(username=username)


def fetch(username: str) -> tuple[int, str, str]:
    return http_client.fetch(LemmyWorldConstants.API_URL.format(username=username))


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    payload = parse.as_json(body)
    if isinstance(payload, dict) and payload.get("error"):
        return VerdictConstants.ABSENT, {}
    if status != 200 or not isinstance(payload, dict):
        return VerdictConstants.UNKNOWN, {}
    view = payload.get("person_view") if isinstance(payload.get("person_view"), dict) else {}
    person = view.get("person") if isinstance(view.get("person"), dict) else {}
    counts = view.get("counts") if isinstance(view.get("counts"), dict) else {}
    if not person.get("name"):
        return VerdictConstants.UNKNOWN, {}
    info = {
        "display_name": parse.clean(person.get("display_name") or person.get("name")),
        "username": parse.text(person.get("name")),
        "description": parse.clean(person.get("bio")),
        "avatar": parse.text(person.get("avatar")),
        "cover": parse.text(person.get("banner")),
        "id": parse.text(counts.get("person_id") or person.get("id")),
        "created_at": parse.text(person.get("published")),
        "posts": parse.text(counts.get("post_count")) if counts.get("post_count") else "",
        "comments": parse.text(counts.get("comment_count")) if counts.get("comment_count") else "",
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    community = re.search(r"/c/([^/?#]+)", final_url or "")
    if community:
        code, payload, _ = http_client.fetch(LemmyWorldConstants.COMMUNITY_API.format(id=community.group(1)))
        data = parse.as_json(payload) if code == 200 else None
        if isinstance(data, dict) and data.get("error"):
            return VerdictConstants.ABSENT, {}
        view = data.get("community_view") if isinstance(data, dict) and isinstance(data.get("community_view"), dict) else {}
        comm = view.get("community") if isinstance(view.get("community"), dict) else {}
        counts = view.get("counts") if isinstance(view.get("counts"), dict) else {}
        if comm.get("name"):
            info = {
                "title": parse.clean(comm.get("title") or comm.get("name")),
                "description": parse.clean(comm.get("description")),
                "image": parse.text(comm.get("icon") or comm.get("banner")),
                "id": parse.text(comm.get("id")),
                "subscribers": parse.text(counts.get("subscribers")) if counts.get("subscribers") else "",
                "posts": parse.text(counts.get("posts")) if counts.get("posts") else "",
            }
            return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    return VerdictConstants.UNKNOWN, {}

ROUTES = (
    ("c/(?P<id>[^/]+)", "group"),
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
