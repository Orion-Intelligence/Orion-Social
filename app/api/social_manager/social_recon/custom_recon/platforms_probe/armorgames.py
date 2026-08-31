from api.social_manager.social_recon.constants.platform_constants import ArmorgamesConstants

constants = ArmorgamesConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
