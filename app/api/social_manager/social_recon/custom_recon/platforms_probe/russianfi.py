from api.social_manager.social_recon.constants.platform_constants import RussianFIConstants

constants = RussianFIConstants

ROUTES = (
    (r"forum/member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
