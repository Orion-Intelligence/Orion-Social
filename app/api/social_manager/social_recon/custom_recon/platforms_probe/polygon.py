from api.social_manager.social_recon.constants.platform_constants import PolygonConstants

constants = PolygonConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
