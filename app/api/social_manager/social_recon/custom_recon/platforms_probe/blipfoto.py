from api.social_manager.social_recon.constants.platform_constants import BlipfotoConstants

constants = BlipfotoConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
