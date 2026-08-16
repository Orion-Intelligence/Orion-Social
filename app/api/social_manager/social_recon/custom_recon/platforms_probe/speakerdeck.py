from api.social_manager.social_recon.constants.platform_constants import SpeakerdeckConstants

constants = SpeakerdeckConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
