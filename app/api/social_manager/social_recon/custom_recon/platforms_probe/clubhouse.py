from api.social_manager.social_recon.constants.platform_constants import ClubhouseConstants

constants = ClubhouseConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
