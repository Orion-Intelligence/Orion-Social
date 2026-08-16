from api.social_manager.social_recon.constants.platform_constants import SlidesConstants

constants = SlidesConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
