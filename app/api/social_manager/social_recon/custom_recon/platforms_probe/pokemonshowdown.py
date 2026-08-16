from api.social_manager.social_recon.constants.platform_constants import PokemonShowdownConstants

constants = PokemonShowdownConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
