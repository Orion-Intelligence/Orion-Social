from api.social_manager.social_recon.constants.platform_constants import AllTheLyricsConstants

constants = AllTheLyricsConstants

ROUTES = (
    (r"forum/member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
