from api.social_manager.social_recon.constants.platform_constants import PCGamerConstants

constants = PCGamerConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
