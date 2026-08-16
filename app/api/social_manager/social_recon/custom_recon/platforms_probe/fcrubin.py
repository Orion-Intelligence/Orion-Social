from api.social_manager.social_recon.constants.platform_constants import FCRubinConstants

constants = FCRubinConstants

ROUTES = (
    (r"forum/member\.php\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
