from api.social_manager.social_recon.constants.platform_constants import DesignspirationConstants

constants = DesignspirationConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
