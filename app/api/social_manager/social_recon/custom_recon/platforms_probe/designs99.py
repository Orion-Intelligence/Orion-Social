from api.social_manager.social_recon.constants.platform_constants import Designs99Constants

constants = Designs99Constants

ROUTES = (
    ("profiles/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
