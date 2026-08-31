from api.social_manager.social_recon.constants.platform_constants import Windows10forumsConstants

constants = Windows10forumsConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
