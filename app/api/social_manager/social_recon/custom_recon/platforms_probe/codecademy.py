from api.social_manager.social_recon.constants.platform_constants import CodecademyConstants

constants = CodecademyConstants

ROUTES = (
    ("profiles/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
