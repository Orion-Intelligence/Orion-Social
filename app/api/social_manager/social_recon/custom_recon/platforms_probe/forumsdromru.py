from api.social_manager.social_recon.constants.platform_constants import ForumsDromRuConstants

constants = ForumsDromRuConstants

ROUTES = (
    (r"member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
