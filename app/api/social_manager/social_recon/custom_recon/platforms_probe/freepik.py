from api.social_manager.social_recon.constants.platform_constants import FreepikConstants

constants = FreepikConstants

ROUTES = (
    ("author/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
