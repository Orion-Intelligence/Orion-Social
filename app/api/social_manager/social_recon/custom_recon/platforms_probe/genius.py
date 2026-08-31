from api.social_manager.social_recon.constants.platform_constants import GeniusConstants

constants = GeniusConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
