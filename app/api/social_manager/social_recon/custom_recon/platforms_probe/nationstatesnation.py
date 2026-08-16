from api.social_manager.social_recon.constants.platform_constants import NationStatesNationConstants

constants = NationStatesNationConstants

ROUTES = (
    ("nation=(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
