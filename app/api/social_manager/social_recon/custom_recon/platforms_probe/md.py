from api.social_manager.social_recon.constants.platform_constants import MdConstants

constants = MdConstants

ROUTES = (
    ("ru/users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
