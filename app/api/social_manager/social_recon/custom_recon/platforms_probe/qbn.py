from api.social_manager.social_recon.constants.platform_constants import QbnConstants

constants = QbnConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
