from api.social_manager.social_recon.constants.platform_constants import FanficslandiaComConstants

constants = FanficslandiaComConstants

ROUTES = (
    (r"index\.php/members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
