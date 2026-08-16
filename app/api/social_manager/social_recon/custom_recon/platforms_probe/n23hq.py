from api.social_manager.social_recon.constants.platform_constants import N23hqConstants

constants = N23hqConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
