from api.social_manager.social_recon.constants.platform_constants import AntiquersConstants

constants = AntiquersConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
