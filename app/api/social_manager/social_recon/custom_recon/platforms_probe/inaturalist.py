from api.social_manager.social_recon.constants.platform_constants import INaturalistConstants

constants = INaturalistConstants

ROUTES = (
    ("lists/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
