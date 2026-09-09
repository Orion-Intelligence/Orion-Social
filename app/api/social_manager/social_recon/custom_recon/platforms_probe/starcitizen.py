import re

import api.social_manager.social_recon.custom_recon.core.parse as parse
from api.social_manager.social_recon.constants.custom_recon_constants import VerdictConstants
from api.social_manager.social_recon.constants.platform_constants import StarCitizenConstants

constants = StarCitizenConstants


def probe_url(username: str) -> str:
    return StarCitizenConstants.PROFILE_URL.format(username=username)


def _image(url: str) -> str:
    value = parse.text(url)
    return "" if parse.is_generic_image(value) else value


def evaluate(status: int, body: str, _final_url: str) -> tuple[str, dict]:
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    pairs = {parse.clean(label).lower(): parse.clean(value) for label, value in re.findall(StarCitizenConstants.PAIRS, body)}
    if "handle name" not in pairs:
        return VerdictConstants.UNKNOWN, {}
    moniker = re.search(StarCitizenConstants.MONIKER, body)
    ranks = re.findall(StarCitizenConstants.RANK, body)
    avatar = re.search(StarCitizenConstants.AVATAR, body)
    bio = re.search(StarCitizenConstants.BIO, body, re.DOTALL)
    org = re.search(r'/orgs/([A-Z0-9]+)"', body)
    info = {
        "display_name": parse.clean(moniker.group(1)) if moniker else pairs.get("handle name"),
        "username": pairs.get("handle name"),
        "description": parse.clean(bio.group(1)) if bio else "",
        "avatar": _image(avatar.group(1)) if avatar else "",
        "id": pairs.get("uee citizen record", "").lstrip("#"),
        "created_at": pairs.get("enlisted", ""),
        "location": re.sub(r"\s*,\s*", ", ", pairs.get("location", "")),
        "fluency": pairs.get("fluency", ""),
        "rank": parse.clean(ranks[0]) if ranks else "",
        "organization": org.group(1) if org else "",
    }
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}


def evaluate_resource(status: int, body: str, final_url: str) -> tuple[str, dict]:
    if status in (404, 410):
        return VerdictConstants.ABSENT, {}
    if status != 200:
        return VerdictConstants.UNKNOWN, {}
    meta = parse.meta(body)
    title = parse.title(body)
    org = re.match(StarCitizenConstants.ORG_TITLE, title)
    members = re.search(StarCitizenConstants.ORG_MEMBERS, body, re.IGNORECASE)
    info = {
        "title": parse.clean(org.group(1)) if org else parse.clean(title.split(" - ")[0]),
        "sid": org.group(2) if org else "",
        "image": _image(meta.get("og:image")),
        "members": members.group(1) if members else "",
    }
    if not info.get("title"):
        return VerdictConstants.UNKNOWN, {}
    return VerdictConstants.EXISTS, {key: value for key, value in info.items() if value}

ROUTES = (
    ("citizens/(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"community\-hub/user/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("orgs/(?P<id>[^/]+)(?:/.*)?", "group"),
)
