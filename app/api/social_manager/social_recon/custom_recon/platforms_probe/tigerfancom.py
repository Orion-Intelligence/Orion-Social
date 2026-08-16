from api.social_manager.social_recon.constants.platform_constants import TigerfanComConstants

constants = TigerfanComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
