from api.social_manager.social_recon.constants.platform_constants import AvforumsConstants

constants = AvforumsConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
