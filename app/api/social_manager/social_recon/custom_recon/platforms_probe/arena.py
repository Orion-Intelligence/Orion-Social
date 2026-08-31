from api.social_manager.social_recon.constants.platform_constants import AreNaConstants

constants = AreNaConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
