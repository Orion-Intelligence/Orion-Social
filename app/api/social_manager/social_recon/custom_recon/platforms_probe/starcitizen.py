from api.social_manager.social_recon.constants.platform_constants import StarCitizenConstants

constants = StarCitizenConstants

ROUTES = (
    ("citizens/(?P<id>[^/]+)(?:/.*)?", "profile"),
    (r"community\-hub/user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
