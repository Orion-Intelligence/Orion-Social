from api.social_manager.social_recon.constants.platform_constants import MyspaceConstants

constants = MyspaceConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
