from api.social_manager.social_recon.constants.platform_constants import WindowsforumConstants

constants = WindowsforumConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
