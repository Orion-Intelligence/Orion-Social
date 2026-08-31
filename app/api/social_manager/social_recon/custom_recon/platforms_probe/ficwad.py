from api.social_manager.social_recon.constants.platform_constants import FicwadConstants

constants = FicwadConstants

ROUTES = (
    ("a/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
