from api.social_manager.social_recon.constants.platform_constants import NextcloudForumConstants

constants = NextcloudForumConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
