from api.social_manager.social_recon.constants.platform_constants import PaltalkConstants

constants = PaltalkConstants

ROUTES = (
    ("people/users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
