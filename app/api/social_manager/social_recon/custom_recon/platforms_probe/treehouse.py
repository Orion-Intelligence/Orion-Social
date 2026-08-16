from api.social_manager.social_recon.constants.platform_constants import TreehouseConstants

constants = TreehouseConstants

ROUTES = (
    ("profiles/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
