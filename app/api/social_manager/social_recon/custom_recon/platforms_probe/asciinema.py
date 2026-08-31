from api.social_manager.social_recon.constants.platform_constants import AsciinemaConstants

constants = AsciinemaConstants

ROUTES = (
    (r"\~(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
