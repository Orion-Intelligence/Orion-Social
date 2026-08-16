from api.social_manager.social_recon.constants.platform_constants import WritingforumsOrgConstants

constants = WritingforumsOrgConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
