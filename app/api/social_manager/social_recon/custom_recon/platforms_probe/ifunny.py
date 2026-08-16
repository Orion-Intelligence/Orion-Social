from api.social_manager.social_recon.constants.platform_constants import IFunnyConstants

constants = IFunnyConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
