from api.social_manager.social_recon.constants.platform_constants import JoyreactorCcConstants

constants = JoyreactorCcConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
