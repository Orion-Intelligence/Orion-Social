from api.social_manager.social_recon.constants.platform_constants import ReplItConstants

constants = ReplItConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
