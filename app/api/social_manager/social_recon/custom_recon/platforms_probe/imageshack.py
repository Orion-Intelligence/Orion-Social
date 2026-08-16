from api.social_manager.social_recon.constants.platform_constants import ImageShackConstants

constants = ImageShackConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
