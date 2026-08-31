from api.social_manager.social_recon.constants.platform_constants import ReplitConstants

constants = ReplitConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
