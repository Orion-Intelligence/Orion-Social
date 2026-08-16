from api.social_manager.social_recon.constants.platform_constants import UvelirConstants

constants = UvelirConstants

ROUTES = (
    (r"member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
