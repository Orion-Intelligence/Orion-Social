from api.social_manager.social_recon.constants.platform_constants import BrusheezyConstants

constants = BrusheezyConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
