from api.social_manager.social_recon.constants.platform_constants import FragmentConstants

constants = FragmentConstants

ROUTES = (
    ("username/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
