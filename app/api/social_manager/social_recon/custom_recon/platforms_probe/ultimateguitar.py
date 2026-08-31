from api.social_manager.social_recon.constants.platform_constants import UltimateGuitarConstants

constants = UltimateGuitarConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
