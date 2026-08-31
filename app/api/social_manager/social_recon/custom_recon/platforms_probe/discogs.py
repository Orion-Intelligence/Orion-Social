from api.social_manager.social_recon.constants.platform_constants import DiscogsConstants

constants = DiscogsConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
