from api.social_manager.social_recon.constants.platform_constants import BuyMeACoffeeConstants

constants = BuyMeACoffeeConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
