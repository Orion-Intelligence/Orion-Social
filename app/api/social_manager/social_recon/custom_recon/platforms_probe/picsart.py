from api.social_manager.social_recon.constants.platform_constants import PicsartConstants

constants = PicsartConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
