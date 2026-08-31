from api.social_manager.social_recon.constants.platform_constants import WeblancerConstants

constants = WeblancerConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
