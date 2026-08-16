from api.social_manager.social_recon.constants.platform_constants import SwedroidSeConstants

constants = SwedroidSeConstants

ROUTES = (
    (r"forum/members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
