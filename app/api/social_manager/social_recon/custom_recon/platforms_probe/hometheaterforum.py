from api.social_manager.social_recon.constants.platform_constants import HometheaterforumConstants

constants = HometheaterforumConstants

ROUTES = (
    (r"community/members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
