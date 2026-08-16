from api.social_manager.social_recon.constants.platform_constants import EthereumMagiciansConstants

constants = EthereumMagiciansConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
