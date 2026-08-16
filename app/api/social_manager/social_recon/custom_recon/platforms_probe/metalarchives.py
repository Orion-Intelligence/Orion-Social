from api.social_manager.social_recon.constants.platform_constants import MetalArchivesConstants

constants = MetalArchivesConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
