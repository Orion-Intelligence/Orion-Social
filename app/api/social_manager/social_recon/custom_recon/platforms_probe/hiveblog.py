from api.social_manager.social_recon.constants.platform_constants import HiveBlogConstants

constants = HiveBlogConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
