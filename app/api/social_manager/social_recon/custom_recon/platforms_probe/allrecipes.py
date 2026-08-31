from api.social_manager.social_recon.constants.platform_constants import AllRecipesConstants

constants = AllRecipesConstants

ROUTES = (
    ("cook/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
