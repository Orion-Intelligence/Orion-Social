from api.social_manager.social_recon.constants.platform_constants import TriplineConstants

constants = TriplineConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
