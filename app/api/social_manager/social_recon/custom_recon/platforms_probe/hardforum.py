from api.social_manager.social_recon.constants.platform_constants import HardforumConstants

constants = HardforumConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
