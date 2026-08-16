from api.social_manager.social_recon.constants.platform_constants import GiantbombConstants

constants = GiantbombConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
