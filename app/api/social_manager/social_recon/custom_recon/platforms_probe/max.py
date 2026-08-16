from api.social_manager.social_recon.constants.platform_constants import MaxConstants

constants = MaxConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
