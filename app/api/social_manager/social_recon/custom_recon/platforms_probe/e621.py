from api.social_manager.social_recon.constants.platform_constants import E621Constants

constants = E621Constants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
