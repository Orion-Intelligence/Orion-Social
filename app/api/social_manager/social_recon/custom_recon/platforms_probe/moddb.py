from api.social_manager.social_recon.constants.platform_constants import ModDBConstants

constants = ModDBConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
