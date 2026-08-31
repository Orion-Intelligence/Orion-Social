from api.social_manager.social_recon.constants.platform_constants import SporcleConstants

constants = SporcleConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
