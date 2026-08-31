from api.social_manager.social_recon.constants.platform_constants import NhattaoComConstants

constants = NhattaoComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
