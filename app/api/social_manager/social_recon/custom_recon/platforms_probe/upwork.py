from api.social_manager.social_recon.constants.platform_constants import UpworkConstants

constants = UpworkConstants

ROUTES = (
    ("fl/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
