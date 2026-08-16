from api.social_manager.social_recon.constants.platform_constants import NikoncafeComConstants

constants = NikoncafeComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
