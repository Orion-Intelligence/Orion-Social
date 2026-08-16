from api.social_manager.social_recon.constants.platform_constants import PeriscopeConstants

constants = PeriscopeConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
