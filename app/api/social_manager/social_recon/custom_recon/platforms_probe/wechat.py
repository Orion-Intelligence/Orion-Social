from api.social_manager.social_recon.constants.platform_constants import WeChatConstants

constants = WeChatConstants

ROUTES = (
    ("(?P<id>[^/]+)", "profile"),
)
