from api.social_manager.social_recon.constants.platform_constants import SpatialConstants

constants = SpatialConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
