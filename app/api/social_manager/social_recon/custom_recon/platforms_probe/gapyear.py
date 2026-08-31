from api.social_manager.social_recon.constants.platform_constants import GapyearConstants

constants = GapyearConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
