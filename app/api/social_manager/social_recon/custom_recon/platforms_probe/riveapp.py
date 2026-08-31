from api.social_manager.social_recon.constants.platform_constants import RiveAppConstants

constants = RiveAppConstants

ROUTES = (
    ("a/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
