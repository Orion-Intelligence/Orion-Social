from api.social_manager.social_recon.constants.platform_constants import ImgflipConstants

constants = ImgflipConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
