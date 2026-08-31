from api.social_manager.social_recon.constants.platform_constants import VLRConstants

constants = VLRConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
