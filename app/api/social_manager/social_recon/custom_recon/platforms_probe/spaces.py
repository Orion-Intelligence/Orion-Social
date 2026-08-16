from api.social_manager.social_recon.constants.platform_constants import SpacesConstants

constants = SpacesConstants

ROUTES = (
    ("mysite/index/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
