from api.social_manager.social_recon.constants.platform_constants import FoursquareConstants

constants = FoursquareConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
