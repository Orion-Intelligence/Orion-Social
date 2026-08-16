from api.social_manager.social_recon.constants.platform_constants import WolpyConstants

constants = WolpyConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
