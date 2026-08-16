from api.social_manager.social_recon.constants.platform_constants import WarframeMarketConstants

constants = WarframeMarketConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
