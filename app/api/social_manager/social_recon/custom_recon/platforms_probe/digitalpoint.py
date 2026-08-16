from api.social_manager.social_recon.constants.platform_constants import DigitalPointConstants

constants = DigitalPointConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
