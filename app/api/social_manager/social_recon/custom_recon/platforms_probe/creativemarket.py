from api.social_manager.social_recon.constants.platform_constants import CreativeMarketConstants

constants = CreativeMarketConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
