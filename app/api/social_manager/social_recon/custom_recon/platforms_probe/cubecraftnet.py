from api.social_manager.social_recon.constants.platform_constants import CubecraftNetConstants

constants = CubecraftNetConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
