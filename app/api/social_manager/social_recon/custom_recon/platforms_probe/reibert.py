from api.social_manager.social_recon.constants.platform_constants import ReibertConstants

constants = ReibertConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
