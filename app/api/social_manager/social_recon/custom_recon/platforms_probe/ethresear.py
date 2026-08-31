from api.social_manager.social_recon.constants.platform_constants import EthresearConstants

constants = EthresearConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
