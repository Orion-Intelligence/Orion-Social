from api.social_manager.social_recon.constants.platform_constants import ChemportConstants

constants = ChemportConstants

ROUTES = (
    (r"forum/memberlist\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
