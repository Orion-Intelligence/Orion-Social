from api.social_manager.social_recon.constants.platform_constants import MydramalistConstants

constants = MydramalistConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
