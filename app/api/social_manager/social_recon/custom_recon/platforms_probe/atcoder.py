from api.social_manager.social_recon.constants.platform_constants import AtcoderConstants

constants = AtcoderConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
