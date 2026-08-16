from api.social_manager.social_recon.constants.platform_constants import WykopConstants

constants = WykopConstants

ROUTES = (
    ("ludzie/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
