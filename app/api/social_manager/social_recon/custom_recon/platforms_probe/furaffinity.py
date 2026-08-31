from api.social_manager.social_recon.constants.platform_constants import FurAffinityConstants

constants = FurAffinityConstants

ROUTES = (
    ("gallery/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
