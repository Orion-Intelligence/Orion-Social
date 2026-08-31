from api.social_manager.social_recon.constants.platform_constants import MobypictureConstants

constants = MobypictureConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
