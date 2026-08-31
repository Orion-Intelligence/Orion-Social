from api.social_manager.social_recon.constants.platform_constants import GaiaOnlineConstants

constants = GaiaOnlineConstants

ROUTES = (
    ("profiles/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
