from api.social_manager.social_recon.constants.platform_constants import JetpunkConstants

constants = JetpunkConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
