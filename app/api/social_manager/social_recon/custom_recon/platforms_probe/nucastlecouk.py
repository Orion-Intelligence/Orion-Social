from api.social_manager.social_recon.constants.platform_constants import NucastleCoUkConstants

constants = NucastleCoUkConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
