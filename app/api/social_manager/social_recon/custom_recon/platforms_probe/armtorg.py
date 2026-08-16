from api.social_manager.social_recon.constants.platform_constants import ArmtorgConstants

constants = ArmtorgConstants

ROUTES = (
    (r"forum/memberlist\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
