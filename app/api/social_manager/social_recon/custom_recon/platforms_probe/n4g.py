from api.social_manager.social_recon.constants.platform_constants import N4gConstants

constants = N4gConstants

ROUTES = (
    ("user/home/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
