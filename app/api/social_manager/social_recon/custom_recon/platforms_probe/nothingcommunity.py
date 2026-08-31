from api.social_manager.social_recon.constants.platform_constants import NothingCommunityConstants

constants = NothingCommunityConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
