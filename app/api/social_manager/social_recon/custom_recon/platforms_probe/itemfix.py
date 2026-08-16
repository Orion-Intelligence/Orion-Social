from api.social_manager.social_recon.constants.platform_constants import ItemFixConstants

constants = ItemFixConstants

ROUTES = (
    ("c/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
