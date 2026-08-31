from api.social_manager.social_recon.constants.platform_constants import W7forumsConstants

constants = W7forumsConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
