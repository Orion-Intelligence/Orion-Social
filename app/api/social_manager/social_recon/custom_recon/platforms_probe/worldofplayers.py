from api.social_manager.social_recon.constants.platform_constants import WorldofplayersConstants

constants = WorldofplayersConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
