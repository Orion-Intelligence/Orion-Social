from api.social_manager.social_recon.constants.platform_constants import OpenGameArtConstants

constants = OpenGameArtConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
