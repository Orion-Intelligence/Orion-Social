from api.social_manager.social_recon.constants.platform_constants import RlocmanConstants

constants = RlocmanConstants

ROUTES = (
    (r"forum/member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
