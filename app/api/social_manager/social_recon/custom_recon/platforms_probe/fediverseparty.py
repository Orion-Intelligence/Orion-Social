from api.social_manager.social_recon.constants.platform_constants import FediversePartyConstants

constants = FediversePartyConstants

ROUTES = (
    ("en/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
