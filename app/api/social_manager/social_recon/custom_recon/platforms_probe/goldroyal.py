from api.social_manager.social_recon.constants.platform_constants import GoldroyalConstants

constants = GoldroyalConstants

ROUTES = (
    (r"member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
