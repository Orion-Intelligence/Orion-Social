from api.social_manager.social_recon.constants.platform_constants import NitroTypeConstants

constants = NitroTypeConstants

ROUTES = (
    ("racer/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
