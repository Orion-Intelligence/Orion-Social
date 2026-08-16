from api.social_manager.social_recon.constants.platform_constants import ThechiveConstants

constants = ThechiveConstants

ROUTES = (
    ("author/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
