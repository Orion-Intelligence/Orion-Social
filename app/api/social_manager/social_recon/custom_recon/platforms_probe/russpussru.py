from api.social_manager.social_recon.constants.platform_constants import RusspussRuConstants

constants = RusspussRuConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
