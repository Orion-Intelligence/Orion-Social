from api.social_manager.social_recon.constants.platform_constants import TeletypeConstants

constants = TeletypeConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
