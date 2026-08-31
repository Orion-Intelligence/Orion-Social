from api.social_manager.social_recon.constants.platform_constants import RappadConstants

constants = RappadConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
