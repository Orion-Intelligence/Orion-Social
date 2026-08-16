from api.social_manager.social_recon.constants.platform_constants import BitBucketConstants

constants = BitBucketConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
