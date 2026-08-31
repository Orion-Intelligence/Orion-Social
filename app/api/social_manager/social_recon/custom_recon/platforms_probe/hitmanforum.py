from api.social_manager.social_recon.constants.platform_constants import HitmanforumConstants

constants = HitmanforumConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
