from api.social_manager.social_recon.constants.platform_constants import ForumJizniConstants

constants = ForumJizniConstants

ROUTES = (
    (r"member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
