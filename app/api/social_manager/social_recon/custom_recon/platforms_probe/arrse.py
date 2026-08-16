from api.social_manager.social_recon.constants.platform_constants import ArrseConstants

constants = ArrseConstants

ROUTES = (
    (r"community/members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
