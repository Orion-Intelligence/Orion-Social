from api.social_manager.social_recon.constants.platform_constants import BigsoccerConstants

constants = BigsoccerConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
