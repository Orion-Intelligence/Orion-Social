from api.social_manager.social_recon.constants.platform_constants import BloggerBloggerComConstants

constants = BloggerBloggerComConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
