from api.social_manager.social_recon.constants.platform_constants import HomebrewtalkComConstants

constants = HomebrewtalkComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
