from api.social_manager.social_recon.constants.platform_constants import AndroidforumsConstants

constants = AndroidforumsConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
