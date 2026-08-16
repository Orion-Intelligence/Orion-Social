from api.social_manager.social_recon.constants.platform_constants import WebdeveloperComConstants

constants = WebdeveloperComConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
