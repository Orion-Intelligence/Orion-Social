from api.social_manager.social_recon.constants.platform_constants import NintendoLifeConstants

constants = NintendoLifeConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
