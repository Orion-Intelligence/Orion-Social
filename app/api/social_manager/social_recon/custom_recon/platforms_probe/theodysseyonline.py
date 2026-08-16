from api.social_manager.social_recon.constants.platform_constants import TheOdysseyOnlineConstants

constants = TheOdysseyOnlineConstants

ROUTES = (
    ("user/@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
