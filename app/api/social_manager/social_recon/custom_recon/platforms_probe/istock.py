from api.social_manager.social_recon.constants.platform_constants import IStockConstants

constants = IStockConstants

ROUTES = (
    ("ru/portfolio/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
