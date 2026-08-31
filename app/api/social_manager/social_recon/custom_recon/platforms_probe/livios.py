from api.social_manager.social_recon.constants.platform_constants import LiviosConstants

constants = LiviosConstants

ROUTES = (
    ("nl/forum/leden/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
