from api.social_manager.social_recon.constants.platform_constants import MuseScoreConstants

constants = MuseScoreConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
