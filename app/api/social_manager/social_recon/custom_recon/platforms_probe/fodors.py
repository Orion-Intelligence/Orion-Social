from api.social_manager.social_recon.constants.platform_constants import FodorsConstants

constants = FodorsConstants

ROUTES = (
    ("community/profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
