from api.social_manager.social_recon.constants.platform_constants import CfdOnlineConstants

constants = CfdOnlineConstants

ROUTES = (
    (r"Forums/members/(?P<id>[^/]+?)\.html", "profile"),
)
