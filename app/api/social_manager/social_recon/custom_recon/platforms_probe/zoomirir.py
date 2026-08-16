from api.social_manager.social_recon.constants.platform_constants import ZoomirIrConstants

constants = ZoomirIrConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
