from api.social_manager.social_recon.constants.platform_constants import PbaseConstants

constants = PbaseConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
