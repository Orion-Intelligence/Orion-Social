from api.social_manager.social_recon.constants.platform_constants import MineplexComConstants

constants = MineplexComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
