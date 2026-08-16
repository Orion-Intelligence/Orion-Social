from api.social_manager.social_recon.constants.platform_constants import SubaruoutbackOrgConstants

constants = SubaruoutbackOrgConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
