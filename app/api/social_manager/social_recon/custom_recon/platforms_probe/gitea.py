from api.social_manager.social_recon.constants.platform_constants import GiteaConstants

constants = GiteaConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
