from api.social_manager.social_recon.constants.platform_constants import DevRantConstants

constants = DevRantConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
