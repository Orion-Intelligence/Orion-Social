from api.social_manager.social_recon.constants.platform_constants import AuConstants

constants = AuConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
