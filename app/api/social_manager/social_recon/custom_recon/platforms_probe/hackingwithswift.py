from api.social_manager.social_recon.constants.platform_constants import HackingWithSwiftConstants

constants = HackingWithSwiftConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
