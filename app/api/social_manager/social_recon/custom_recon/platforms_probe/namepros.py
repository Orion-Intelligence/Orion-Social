from api.social_manager.social_recon.constants.platform_constants import NameprosConstants

constants = NameprosConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
