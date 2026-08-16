from api.social_manager.social_recon.constants.platform_constants import ChatujmeCzConstants

constants = ChatujmeCzConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
