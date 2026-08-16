from api.social_manager.social_recon.constants.platform_constants import ForumHrConstants

constants = ForumHrConstants

ROUTES = (
    (r"member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
