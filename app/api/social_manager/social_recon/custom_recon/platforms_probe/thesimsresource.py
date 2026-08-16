from api.social_manager.social_recon.constants.platform_constants import TheSimsResourceConstants

constants = TheSimsResourceConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
