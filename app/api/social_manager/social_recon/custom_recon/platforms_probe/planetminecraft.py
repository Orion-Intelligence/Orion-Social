from api.social_manager.social_recon.constants.platform_constants import PlanetMinecraftConstants

constants = PlanetMinecraftConstants

ROUTES = (
    ("member/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
