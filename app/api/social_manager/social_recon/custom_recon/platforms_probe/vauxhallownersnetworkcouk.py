from api.social_manager.social_recon.constants.platform_constants import VauxhallownersnetworkCoUkConstants

constants = VauxhallownersnetworkCoUkConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
