from api.social_manager.social_recon.constants.platform_constants import WarpcastConstants

constants = WarpcastConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
