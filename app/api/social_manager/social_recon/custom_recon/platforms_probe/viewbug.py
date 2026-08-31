from api.social_manager.social_recon.constants.platform_constants import ViewBugConstants

constants = ViewBugConstants

ROUTES = (
    ("member/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
