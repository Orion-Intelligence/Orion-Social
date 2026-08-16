from api.social_manager.social_recon.constants.platform_constants import SvtperformanceComConstants

constants = SvtperformanceComConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
