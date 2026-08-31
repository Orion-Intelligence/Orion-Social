from api.social_manager.social_recon.constants.platform_constants import LyricsTranslateConstants

constants = LyricsTranslateConstants

ROUTES = (
    ("sco/translator/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
