from api.social_manager.social_recon.constants.platform_constants import NoblogsConstants

constants = NoblogsConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
