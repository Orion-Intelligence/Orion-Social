from api.social_manager.social_recon.constants.platform_constants import N1001tracklistsConstants

constants = N1001tracklistsConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
