from api.social_manager.social_recon.constants.platform_constants import XgmGuruConstants

constants = XgmGuruConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
