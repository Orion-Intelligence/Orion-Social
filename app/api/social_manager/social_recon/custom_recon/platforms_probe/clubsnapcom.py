from api.social_manager.social_recon.constants.platform_constants import ClubsnapComConstants

constants = ClubsnapComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
