from api.social_manager.social_recon.constants.platform_constants import MstdnIoConstants

constants = MstdnIoConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
