from api.social_manager.social_recon.constants.platform_constants import DLiveConstants

constants = DLiveConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
