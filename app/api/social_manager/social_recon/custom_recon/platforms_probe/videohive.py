from api.social_manager.social_recon.constants.platform_constants import VideoHiveConstants

constants = VideoHiveConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
