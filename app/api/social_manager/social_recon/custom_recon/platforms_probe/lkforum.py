from api.social_manager.social_recon.constants.platform_constants import LkforumConstants

constants = LkforumConstants

ROUTES = (
    (r"member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
