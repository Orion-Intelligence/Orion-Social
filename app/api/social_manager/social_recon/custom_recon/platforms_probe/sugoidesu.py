from api.social_manager.social_recon.constants.platform_constants import SugoidesuConstants

constants = SugoidesuConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
