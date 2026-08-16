from api.social_manager.social_recon.constants.platform_constants import AffiliatefixConstants

constants = AffiliatefixConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
