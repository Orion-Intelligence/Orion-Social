from api.social_manager.social_recon.constants.platform_constants import ThoughtsComConstants

constants = ThoughtsComConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
