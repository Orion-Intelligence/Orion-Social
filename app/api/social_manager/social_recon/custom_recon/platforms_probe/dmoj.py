from api.social_manager.social_recon.constants.platform_constants import DMOJConstants

constants = DMOJConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
