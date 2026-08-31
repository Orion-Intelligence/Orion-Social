from api.social_manager.social_recon.constants.platform_constants import TopcoderConstants

constants = TopcoderConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
