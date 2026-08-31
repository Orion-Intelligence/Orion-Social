from api.social_manager.social_recon.constants.platform_constants import RailforumsCoUkConstants

constants = RailforumsCoUkConstants

ROUTES = (
    (r"members\?(?:.*&)?username=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
