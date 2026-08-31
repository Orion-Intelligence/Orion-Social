from api.social_manager.social_recon.constants.platform_constants import ClozemasterConstants

constants = ClozemasterConstants

ROUTES = (
    ("players/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
