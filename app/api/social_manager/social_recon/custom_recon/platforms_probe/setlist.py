from api.social_manager.social_recon.constants.platform_constants import SetlistConstants

constants = SetlistConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
