from api.social_manager.social_recon.constants.platform_constants import GovloopConstants

constants = GovloopConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
