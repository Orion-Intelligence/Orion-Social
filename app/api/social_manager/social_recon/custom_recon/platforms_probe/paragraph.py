from api.social_manager.social_recon.constants.platform_constants import ParagraphConstants

constants = ParagraphConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
