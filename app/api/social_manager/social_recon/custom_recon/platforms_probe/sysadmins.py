from api.social_manager.social_recon.constants.platform_constants import SysadminsConstants

constants = SysadminsConstants

ROUTES = (
    (r"member(?P<id>[^/]+?)\.html", "profile"),
)
