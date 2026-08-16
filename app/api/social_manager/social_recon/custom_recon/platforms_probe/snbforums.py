from api.social_manager.social_recon.constants.platform_constants import SnbforumsConstants

constants = SnbforumsConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
