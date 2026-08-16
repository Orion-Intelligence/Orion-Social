from api.social_manager.social_recon.constants.platform_constants import NamuwikiConstants

constants = NamuwikiConstants

ROUTES = (
    ("w/사용자:(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
