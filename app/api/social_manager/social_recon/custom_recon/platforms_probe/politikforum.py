from api.social_manager.social_recon.constants.platform_constants import PolitikforumConstants

constants = PolitikforumConstants

ROUTES = (
    (r"member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
