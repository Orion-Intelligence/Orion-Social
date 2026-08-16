from api.social_manager.social_recon.constants.platform_constants import JeepgarageOrgConstants

constants = JeepgarageOrgConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
