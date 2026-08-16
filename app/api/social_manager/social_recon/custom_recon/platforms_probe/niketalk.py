from api.social_manager.social_recon.constants.platform_constants import NiketalkConstants

constants = NiketalkConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
