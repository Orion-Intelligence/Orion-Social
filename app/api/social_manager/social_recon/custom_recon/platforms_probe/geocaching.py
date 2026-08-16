from api.social_manager.social_recon.constants.platform_constants import GeocachingConstants

constants = GeocachingConstants

ROUTES = (
    (r"p\?(?:.*&)?u=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
