from api.social_manager.social_recon.constants.platform_constants import VgtimesGamesConstants

constants = VgtimesGamesConstants

ROUTES = (
    ("games/(?P<id>[^/]+)(?:/.*)?", "profile"),
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
