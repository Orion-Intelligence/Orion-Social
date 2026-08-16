from api.social_manager.social_recon.constants.platform_constants import SamlibConstants

constants = SamlibConstants

ROUTES = (
    ("e/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
