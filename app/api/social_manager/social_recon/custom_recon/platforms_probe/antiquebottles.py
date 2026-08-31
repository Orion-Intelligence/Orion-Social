from api.social_manager.social_recon.constants.platform_constants import AntiqueBottlesConstants

constants = AntiqueBottlesConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
