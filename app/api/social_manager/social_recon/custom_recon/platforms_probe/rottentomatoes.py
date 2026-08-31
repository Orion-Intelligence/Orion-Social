from api.social_manager.social_recon.constants.platform_constants import RottentomatoesConstants

constants = RottentomatoesConstants

ROUTES = (
    ("critic/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
