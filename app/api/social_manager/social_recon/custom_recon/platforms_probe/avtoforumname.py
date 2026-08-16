from api.social_manager.social_recon.constants.platform_constants import AvtoForumNameConstants

constants = AvtoForumNameConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
