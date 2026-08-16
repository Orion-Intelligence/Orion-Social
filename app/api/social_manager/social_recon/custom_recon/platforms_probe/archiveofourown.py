from api.social_manager.social_recon.constants.platform_constants import ArchiveOfOurOwnConstants

constants = ArchiveOfOurOwnConstants

ROUTES = (
    ("users/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
