from api.social_manager.social_recon.constants.platform_constants import NPMConstants

constants = NPMConstants

ROUTES = (
    (r"\~(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
