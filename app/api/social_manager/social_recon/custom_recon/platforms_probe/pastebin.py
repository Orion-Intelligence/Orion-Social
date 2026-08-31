from api.social_manager.social_recon.constants.platform_constants import PastebinConstants

constants = PastebinConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
