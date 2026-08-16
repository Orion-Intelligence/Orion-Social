from api.social_manager.social_recon.constants.platform_constants import ViberConstants

constants = ViberConstants

ROUTES = (
    (r"\?g2=(?P<id>[^&]+)(?:&.*)?", "group"),
)
