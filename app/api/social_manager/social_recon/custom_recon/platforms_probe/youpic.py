from api.social_manager.social_recon.constants.platform_constants import YouPicConstants

constants = YouPicConstants

ROUTES = (
    ("photographer/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
