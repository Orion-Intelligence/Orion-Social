from api.social_manager.social_recon.constants.platform_constants import CoroflotConstants

constants = CoroflotConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
