from api.social_manager.social_recon.constants.platform_constants import LightstalkingComConstants

constants = LightstalkingComConstants

ROUTES = (
    ("author/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
