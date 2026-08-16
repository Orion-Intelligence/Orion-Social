from api.social_manager.social_recon.constants.platform_constants import ImoodConstants

constants = ImoodConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
