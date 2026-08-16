from api.social_manager.social_recon.constants.platform_constants import CodersRankConstants

constants = CodersRankConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
