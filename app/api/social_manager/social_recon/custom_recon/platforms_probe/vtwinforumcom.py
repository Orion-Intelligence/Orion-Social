from api.social_manager.social_recon.constants.platform_constants import VTwinforumComConstants

constants = VTwinforumComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
