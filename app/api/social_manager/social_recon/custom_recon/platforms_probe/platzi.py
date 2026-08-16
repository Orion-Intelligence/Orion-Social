from api.social_manager.social_recon.constants.platform_constants import PlatziConstants

constants = PlatziConstants

ROUTES = (
    ("p/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
