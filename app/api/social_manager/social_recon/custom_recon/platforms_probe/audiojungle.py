from api.social_manager.social_recon.constants.platform_constants import AudiojungleConstants

constants = AudiojungleConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
