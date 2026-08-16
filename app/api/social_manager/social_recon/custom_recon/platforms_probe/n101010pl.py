from api.social_manager.social_recon.constants.platform_constants import N101010PlConstants

constants = N101010PlConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
