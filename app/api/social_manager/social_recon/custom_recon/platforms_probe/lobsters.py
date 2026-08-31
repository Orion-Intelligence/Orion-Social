from api.social_manager.social_recon.constants.platform_constants import LobstersConstants

constants = LobstersConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
