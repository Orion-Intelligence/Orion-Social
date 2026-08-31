from api.social_manager.social_recon.constants.platform_constants import ResidentAdvisorConstants

constants = ResidentAdvisorConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
