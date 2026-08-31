from api.social_manager.social_recon.constants.platform_constants import VoicesConstants

constants = VoicesConstants

ROUTES = (
    ("actors/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
