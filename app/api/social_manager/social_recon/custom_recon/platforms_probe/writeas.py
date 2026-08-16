from api.social_manager.social_recon.constants.platform_constants import WriteAsConstants

constants = WriteAsConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
