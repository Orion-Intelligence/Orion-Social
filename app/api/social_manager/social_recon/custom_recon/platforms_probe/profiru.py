from api.social_manager.social_recon.constants.platform_constants import ProfiRuConstants

constants = ProfiRuConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
