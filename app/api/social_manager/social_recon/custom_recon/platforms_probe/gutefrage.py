from api.social_manager.social_recon.constants.platform_constants import GutefrageConstants

constants = GutefrageConstants

ROUTES = (
    ("nutzer/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
