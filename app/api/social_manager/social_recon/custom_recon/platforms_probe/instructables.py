from api.social_manager.social_recon.constants.platform_constants import InstructablesConstants

constants = InstructablesConstants

ROUTES = (
    ("member/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
