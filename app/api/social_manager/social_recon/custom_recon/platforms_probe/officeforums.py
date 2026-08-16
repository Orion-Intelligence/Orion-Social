from api.social_manager.social_recon.constants.platform_constants import OfficeForumsConstants

constants = OfficeForumsConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
