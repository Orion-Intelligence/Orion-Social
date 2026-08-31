from api.social_manager.social_recon.constants.platform_constants import ListographyConstants

constants = ListographyConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
