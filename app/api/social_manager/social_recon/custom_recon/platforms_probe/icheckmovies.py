from api.social_manager.social_recon.constants.platform_constants import IcheckmoviesConstants

constants = IcheckmoviesConstants

ROUTES = (
    ("profiles/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
