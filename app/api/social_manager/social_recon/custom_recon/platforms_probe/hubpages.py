from api.social_manager.social_recon.constants.platform_constants import HubPagesConstants

constants = HubPagesConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
