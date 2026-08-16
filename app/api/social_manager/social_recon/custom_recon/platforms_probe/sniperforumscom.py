from api.social_manager.social_recon.constants.platform_constants import SniperforumsComConstants

constants = SniperforumsComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
