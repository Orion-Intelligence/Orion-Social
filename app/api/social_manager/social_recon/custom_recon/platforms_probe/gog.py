from api.social_manager.social_recon.constants.platform_constants import GogConstants

constants = GogConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
