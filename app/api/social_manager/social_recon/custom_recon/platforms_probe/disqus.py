from api.social_manager.social_recon.constants.platform_constants import DisqusConstants

constants = DisqusConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
