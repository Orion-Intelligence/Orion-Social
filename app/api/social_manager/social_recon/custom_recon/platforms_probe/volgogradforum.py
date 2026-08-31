from api.social_manager.social_recon.constants.platform_constants import VolgogradForumConstants

constants = VolgogradForumConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
