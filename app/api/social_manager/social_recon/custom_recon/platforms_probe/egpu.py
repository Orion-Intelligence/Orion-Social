from api.social_manager.social_recon.constants.platform_constants import EGPUConstants

constants = EGPUConstants

ROUTES = (
    ("forums/profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
