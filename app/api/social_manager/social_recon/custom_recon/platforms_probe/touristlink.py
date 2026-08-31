from api.social_manager.social_recon.constants.platform_constants import TouristlinkConstants

constants = TouristlinkConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
