from api.social_manager.social_recon.constants.platform_constants import RollitupConstants

constants = RollitupConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
