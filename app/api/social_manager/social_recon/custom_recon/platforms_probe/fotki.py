from api.social_manager.social_recon.constants.platform_constants import FotkiConstants

constants = FotkiConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
