from api.social_manager.social_recon.constants.platform_constants import TinderConstants

constants = TinderConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
