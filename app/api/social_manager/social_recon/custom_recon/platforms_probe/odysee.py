from api.social_manager.social_recon.constants.platform_constants import OdyseeConstants

constants = OdyseeConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
