from api.social_manager.social_recon.constants.platform_constants import UstreamConstants

constants = UstreamConstants

ROUTES = (
    ("channel/adam(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
