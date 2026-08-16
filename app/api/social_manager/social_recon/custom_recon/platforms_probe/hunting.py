from api.social_manager.social_recon.constants.platform_constants import HuntingConstants

constants = HuntingConstants

ROUTES = (
    (r"forum/members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
