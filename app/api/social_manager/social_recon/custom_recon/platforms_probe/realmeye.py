from api.social_manager.social_recon.constants.platform_constants import RealmeyeConstants

constants = RealmeyeConstants

ROUTES = (
    ("player/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
