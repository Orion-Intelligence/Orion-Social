from api.social_manager.social_recon.constants.platform_constants import OakleyforumComConstants

constants = OakleyforumComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
