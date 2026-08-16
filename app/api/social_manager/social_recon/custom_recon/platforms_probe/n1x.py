from api.social_manager.social_recon.constants.platform_constants import N1xConstants

constants = N1xConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
