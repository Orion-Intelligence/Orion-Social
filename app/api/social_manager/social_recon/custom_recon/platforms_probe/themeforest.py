from api.social_manager.social_recon.constants.platform_constants import ThemeForestConstants

constants = ThemeForestConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
