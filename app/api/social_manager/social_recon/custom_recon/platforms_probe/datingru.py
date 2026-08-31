from api.social_manager.social_recon.constants.platform_constants import DatingRuConstants

constants = DatingRuConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
