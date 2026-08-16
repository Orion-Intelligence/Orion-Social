from api.social_manager.social_recon.constants.platform_constants import NaverCafeConstants

constants = NaverCafeConstants

ROUTES = (
    (r"(?P<id>[^/]+)/(?P<post>\d+)", "post"),
    ("(?P<id>[^/]+)", "group"),
)
