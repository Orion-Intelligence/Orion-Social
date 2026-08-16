from api.social_manager.social_recon.constants.platform_constants import WeforumConstants

constants = WeforumConstants

ROUTES = (
    ("people/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
