from api.social_manager.social_recon.constants.platform_constants import PlingConstants

constants = PlingConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
