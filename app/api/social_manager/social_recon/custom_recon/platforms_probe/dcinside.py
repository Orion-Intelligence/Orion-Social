from api.social_manager.social_recon.constants.platform_constants import DcinsideConstants

constants = DcinsideConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
