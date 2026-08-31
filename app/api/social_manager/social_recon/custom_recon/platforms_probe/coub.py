from api.social_manager.social_recon.constants.platform_constants import CoubConstants

constants = CoubConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
