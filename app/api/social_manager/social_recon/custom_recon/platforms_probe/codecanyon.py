from api.social_manager.social_recon.constants.platform_constants import CodecanyonConstants

constants = CodecanyonConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
