from api.social_manager.social_recon.constants.platform_constants import TruthbookConstants

constants = TruthbookConstants

ROUTES = (
    (r"forum/memberlist\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
