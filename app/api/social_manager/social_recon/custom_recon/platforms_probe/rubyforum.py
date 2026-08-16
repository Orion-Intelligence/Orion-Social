from api.social_manager.social_recon.constants.platform_constants import RubyForumConstants

constants = RubyForumConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
