from api.social_manager.social_recon.constants.platform_constants import PokecommunityConstants

constants = PokecommunityConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
