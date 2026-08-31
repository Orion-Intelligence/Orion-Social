from api.social_manager.social_recon.constants.platform_constants import FreesoundConstants

constants = FreesoundConstants

ROUTES = (
    ("people/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
