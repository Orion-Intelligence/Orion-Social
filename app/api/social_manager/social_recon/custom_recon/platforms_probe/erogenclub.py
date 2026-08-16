from api.social_manager.social_recon.constants.platform_constants import ErogenClubConstants

constants = ErogenClubConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
