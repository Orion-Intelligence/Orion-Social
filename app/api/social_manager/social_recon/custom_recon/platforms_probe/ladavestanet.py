from api.social_manager.social_recon.constants.platform_constants import LadaVestaNetConstants

constants = LadaVestaNetConstants

ROUTES = (
    (r"member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
