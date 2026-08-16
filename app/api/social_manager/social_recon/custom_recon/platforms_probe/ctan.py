from api.social_manager.social_recon.constants.platform_constants import CTANConstants

constants = CTANConstants

ROUTES = (
    ("author/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
