from api.social_manager.social_recon.constants.platform_constants import RidemonkeyComConstants

constants = RidemonkeyComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
