from api.social_manager.social_recon.constants.platform_constants import PixelfedSocialConstants

constants = PixelfedSocialConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
