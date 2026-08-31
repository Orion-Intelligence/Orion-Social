from api.social_manager.social_recon.constants.platform_constants import NeoseekerConstants

constants = NeoseekerConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
