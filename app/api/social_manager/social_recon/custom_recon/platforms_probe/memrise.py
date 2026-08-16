from api.social_manager.social_recon.constants.platform_constants import MemriseConstants

constants = MemriseConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
