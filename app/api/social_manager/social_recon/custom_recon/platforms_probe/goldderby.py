from api.social_manager.social_recon.constants.platform_constants import GoldderbyConstants

constants = GoldderbyConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
