from api.social_manager.social_recon.constants.platform_constants import LineConstants

constants = LineConstants

ROUTES = (
    ("(?:R/)?ti/p/(?P<id>[^/]+)", "profile"),
    ("(?:R/)?ti/g/(?P<id>[^/]+)", "group"),
)
