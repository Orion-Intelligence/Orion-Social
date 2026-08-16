from api.social_manager.social_recon.constants.platform_constants import SourceForgeConstants

constants = SourceForgeConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
