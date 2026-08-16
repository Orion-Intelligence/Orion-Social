from api.social_manager.social_recon.constants.platform_constants import TvGamesConstants

constants = TvGamesConstants

ROUTES = (
    (r"forum/member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
