from api.social_manager.social_recon.constants.platform_constants import IfishNetConstants

constants = IfishNetConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
