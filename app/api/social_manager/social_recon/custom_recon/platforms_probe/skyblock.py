from api.social_manager.social_recon.constants.platform_constants import SkyblockConstants

constants = SkyblockConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
