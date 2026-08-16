from api.social_manager.social_recon.constants.platform_constants import PronounsPageConstants

constants = PronounsPageConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
