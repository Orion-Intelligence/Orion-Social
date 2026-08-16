from api.social_manager.social_recon.constants.platform_constants import GeeksforGeeksConstants

constants = GeeksforGeeksConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
