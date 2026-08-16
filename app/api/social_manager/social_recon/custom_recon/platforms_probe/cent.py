from api.social_manager.social_recon.constants.platform_constants import CentConstants

constants = CentConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
