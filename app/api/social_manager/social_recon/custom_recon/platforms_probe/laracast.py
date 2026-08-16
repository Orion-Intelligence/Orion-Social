from api.social_manager.social_recon.constants.platform_constants import LaracastConstants

constants = LaracastConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
