from api.social_manager.social_recon.constants.platform_constants import XtratimeOrgConstants

constants = XtratimeOrgConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
