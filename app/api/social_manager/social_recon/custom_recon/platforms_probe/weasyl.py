from api.social_manager.social_recon.constants.platform_constants import WeasylConstants

constants = WeasylConstants

ROUTES = (
    (r"\~(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
