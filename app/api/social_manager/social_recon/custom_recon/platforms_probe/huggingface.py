from api.social_manager.social_recon.constants.platform_constants import HuggingFaceConstants

constants = HuggingFaceConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
