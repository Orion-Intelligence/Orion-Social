from api.social_manager.social_recon.constants.platform_constants import CoderwallConstants

constants = CoderwallConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
