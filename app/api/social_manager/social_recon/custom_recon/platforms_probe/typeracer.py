from api.social_manager.social_recon.constants.platform_constants import TyperacerConstants

constants = TyperacerConstants

ROUTES = (
    (r"pit/profile\?(?:.*&)?user=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
