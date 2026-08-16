from api.social_manager.social_recon.constants.platform_constants import ShowmeConstants

constants = ShowmeConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
