from api.social_manager.social_recon.constants.platform_constants import JigidiConstants

constants = JigidiConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
