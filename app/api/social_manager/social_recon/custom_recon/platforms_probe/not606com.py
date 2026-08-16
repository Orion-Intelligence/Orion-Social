from api.social_manager.social_recon.constants.platform_constants import Not606ComConstants

constants = Not606ComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
