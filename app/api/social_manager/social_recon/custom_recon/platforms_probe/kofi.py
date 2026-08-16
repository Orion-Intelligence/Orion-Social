from api.social_manager.social_recon.constants.platform_constants import KofiConstants

constants = KofiConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
