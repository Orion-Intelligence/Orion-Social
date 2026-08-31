from api.social_manager.social_recon.constants.platform_constants import CowboyszoneComConstants

constants = CowboyszoneComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
