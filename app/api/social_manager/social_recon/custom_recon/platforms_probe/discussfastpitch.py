from api.social_manager.social_recon.constants.platform_constants import DiscussfastpitchConstants

constants = DiscussfastpitchConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
