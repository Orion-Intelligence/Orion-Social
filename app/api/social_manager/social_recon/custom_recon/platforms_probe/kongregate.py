from api.social_manager.social_recon.constants.platform_constants import KongregateConstants

constants = KongregateConstants

ROUTES = (
    ("accounts/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
