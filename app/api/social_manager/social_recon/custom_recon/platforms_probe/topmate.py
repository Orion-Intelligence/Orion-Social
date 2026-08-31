from api.social_manager.social_recon.constants.platform_constants import TopmateConstants

constants = TopmateConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
