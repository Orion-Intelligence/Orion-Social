from api.social_manager.social_recon.constants.platform_constants import GoodgameRuConstants

constants = GoodgameRuConstants

ROUTES = (
    ("channel/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
