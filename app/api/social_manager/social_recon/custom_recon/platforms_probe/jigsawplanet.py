from api.social_manager.social_recon.constants.platform_constants import JigsawplanetConstants

constants = JigsawplanetConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
