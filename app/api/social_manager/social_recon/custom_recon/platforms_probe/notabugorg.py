from api.social_manager.social_recon.constants.platform_constants import NotabugOrgConstants

constants = NotabugOrgConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
