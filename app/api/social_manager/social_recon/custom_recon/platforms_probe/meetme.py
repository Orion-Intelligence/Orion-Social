from api.social_manager.social_recon.constants.platform_constants import MeetMeConstants

constants = MeetMeConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
