from api.social_manager.social_recon.constants.platform_constants import CryptoHackConstants

constants = CryptoHackConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
