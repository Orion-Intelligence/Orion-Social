from api.social_manager.social_recon.constants.platform_constants import RedcafeConstants

constants = RedcafeConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
