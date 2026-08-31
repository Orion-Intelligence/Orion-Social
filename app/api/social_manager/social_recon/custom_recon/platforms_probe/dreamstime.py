from api.social_manager.social_recon.constants.platform_constants import DreamstimeConstants

constants = DreamstimeConstants

ROUTES = (
    ("(?P<id>[^/]+?)_info", "profile"),
)
