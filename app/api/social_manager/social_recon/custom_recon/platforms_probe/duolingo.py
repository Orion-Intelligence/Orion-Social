from api.social_manager.social_recon.constants.platform_constants import DuolingoConstants

constants = DuolingoConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
