from api.social_manager.social_recon.constants.platform_constants import ElixirforumConstants

constants = ElixirforumConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
