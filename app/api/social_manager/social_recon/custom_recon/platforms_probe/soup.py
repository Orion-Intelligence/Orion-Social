from api.social_manager.social_recon.constants.platform_constants import SoupConstants

constants = SoupConstants

ROUTES = (
    ("author/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
