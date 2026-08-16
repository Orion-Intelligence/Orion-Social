from api.social_manager.social_recon.constants.platform_constants import GuruShotsConstants

constants = GuruShotsConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
