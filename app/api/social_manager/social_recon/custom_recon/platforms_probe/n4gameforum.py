from api.social_manager.social_recon.constants.platform_constants import N4gameforumConstants

constants = N4gameforumConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
