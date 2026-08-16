from api.social_manager.social_recon.constants.platform_constants import MynicknameComConstants

constants = MynicknameComConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
