from api.social_manager.social_recon.constants.platform_constants import SportsRuConstants

constants = SportsRuConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
