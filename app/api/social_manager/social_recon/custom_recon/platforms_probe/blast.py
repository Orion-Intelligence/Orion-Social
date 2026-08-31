from api.social_manager.social_recon.constants.platform_constants import BlastConstants

constants = BlastConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
