from api.social_manager.social_recon.constants.platform_constants import MacosxConstants

constants = MacosxConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
