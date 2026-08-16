from api.social_manager.social_recon.constants.platform_constants import WowheadConstants

constants = WowheadConstants

ROUTES = (
    ("user=(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
