from api.social_manager.social_recon.constants.platform_constants import PolitforumsConstants

constants = PolitforumsConstants

ROUTES = (
    (r"free/profile\.php\?(?:.*&)?showuser=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
