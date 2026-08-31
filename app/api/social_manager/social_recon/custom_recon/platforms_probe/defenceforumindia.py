from api.social_manager.social_recon.constants.platform_constants import DefenceForumIndiaConstants

constants = DefenceForumIndiaConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
