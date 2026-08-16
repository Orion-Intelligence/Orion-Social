from api.social_manager.social_recon.constants.platform_constants import JSFiddleConstants

constants = JSFiddleConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
