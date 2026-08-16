from api.social_manager.social_recon.constants.platform_constants import GuruConstants

constants = GuruConstants

ROUTES = (
    ("freelancers/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
