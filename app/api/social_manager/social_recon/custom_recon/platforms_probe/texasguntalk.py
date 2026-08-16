from api.social_manager.social_recon.constants.platform_constants import TexasguntalkConstants

constants = TexasguntalkConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
