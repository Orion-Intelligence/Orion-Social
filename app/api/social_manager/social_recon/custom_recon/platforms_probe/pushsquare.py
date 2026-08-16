from api.social_manager.social_recon.constants.platform_constants import PushSquareConstants

constants = PushSquareConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
