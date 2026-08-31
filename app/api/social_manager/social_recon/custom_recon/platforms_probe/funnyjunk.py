from api.social_manager.social_recon.constants.platform_constants import FunnyjunkConstants

constants = FunnyjunkConstants

ROUTES = (
    ("user/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
