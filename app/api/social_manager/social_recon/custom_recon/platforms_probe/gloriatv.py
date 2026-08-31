from api.social_manager.social_recon.constants.platform_constants import GloriaTvConstants

constants = GloriaTvConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
