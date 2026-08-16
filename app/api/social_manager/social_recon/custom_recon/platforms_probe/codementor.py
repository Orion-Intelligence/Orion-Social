from api.social_manager.social_recon.constants.platform_constants import CodementorConstants

constants = CodementorConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
