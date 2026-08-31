from api.social_manager.social_recon.constants.platform_constants import VintageMustangComConstants

constants = VintageMustangComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
