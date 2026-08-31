from api.social_manager.social_recon.constants.platform_constants import PinkbikeConstants

constants = PinkbikeConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
