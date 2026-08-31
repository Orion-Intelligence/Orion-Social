from api.social_manager.social_recon.constants.platform_constants import SmokingmeatforumsComConstants

constants = SmokingmeatforumsComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
