from api.social_manager.social_recon.constants.platform_constants import LemmyWorldConstants

constants = LemmyWorldConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
