from api.social_manager.social_recon.constants.platform_constants import OpenCollectiveConstants

constants = OpenCollectiveConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
