from api.social_manager.social_recon.constants.platform_constants import GpodderConstants

constants = GpodderConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
