from api.social_manager.social_recon.constants.platform_constants import SubaruforesterOrgConstants

constants = SubaruforesterOrgConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
