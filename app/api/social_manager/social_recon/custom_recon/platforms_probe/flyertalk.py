from api.social_manager.social_recon.constants.platform_constants import FlyertalkConstants

constants = FlyertalkConstants

ROUTES = (
    (r"forum/members/(?P<id>[^/]+?)\.html", "profile"),
)
