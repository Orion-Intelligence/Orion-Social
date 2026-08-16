from api.social_manager.social_recon.constants.platform_constants import DigitalOceanConstants

constants = DigitalOceanConstants

ROUTES = (
    ("community/users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
