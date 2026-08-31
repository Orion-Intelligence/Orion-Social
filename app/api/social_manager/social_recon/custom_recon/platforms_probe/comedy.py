from api.social_manager.social_recon.constants.platform_constants import ComedyConstants

constants = ComedyConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
