from api.social_manager.social_recon.constants.platform_constants import StihiRuConstants

constants = StihiRuConstants

ROUTES = (
    ("avtor/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
