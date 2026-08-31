from api.social_manager.social_recon.constants.platform_constants import GBAtempNetConstants

constants = GBAtempNetConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
