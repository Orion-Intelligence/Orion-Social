from api.social_manager.social_recon.constants.platform_constants import ChangeOrgConstants

constants = ChangeOrgConstants

ROUTES = (
    ("o/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
