from api.social_manager.social_recon.constants.platform_constants import OpenSourceConstants

constants = OpenSourceConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
