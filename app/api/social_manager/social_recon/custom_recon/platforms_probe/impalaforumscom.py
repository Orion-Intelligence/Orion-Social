from api.social_manager.social_recon.constants.platform_constants import ImpalaforumsComConstants

constants = ImpalaforumsComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
