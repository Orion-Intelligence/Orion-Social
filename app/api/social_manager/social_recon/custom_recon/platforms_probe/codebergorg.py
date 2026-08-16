from api.social_manager.social_recon.constants.platform_constants import CodebergOrgConstants

constants = CodebergOrgConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
