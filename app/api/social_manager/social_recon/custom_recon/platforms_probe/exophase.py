from api.social_manager.social_recon.constants.platform_constants import ExophaseConstants

constants = ExophaseConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
