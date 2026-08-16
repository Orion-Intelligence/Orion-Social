from api.social_manager.social_recon.constants.platform_constants import ProzaRuConstants

constants = ProzaRuConstants

ROUTES = (
    ("avtor/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
