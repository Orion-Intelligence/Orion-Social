from api.social_manager.social_recon.constants.platform_constants import GvectorsConstants

constants = GvectorsConstants

ROUTES = (
    ("forum/profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
