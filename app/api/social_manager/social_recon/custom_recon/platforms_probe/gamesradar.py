from api.social_manager.social_recon.constants.platform_constants import GamesRadarConstants

constants = GamesRadarConstants

ROUTES = (
    ("uk/author/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
