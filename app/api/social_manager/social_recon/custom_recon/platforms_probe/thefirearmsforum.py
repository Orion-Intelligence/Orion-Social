from api.social_manager.social_recon.constants.platform_constants import ThefirearmsforumConstants

constants = ThefirearmsforumConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
