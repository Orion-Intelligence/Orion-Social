from api.social_manager.social_recon.constants.platform_constants import MonkeytypeConstants

constants = MonkeytypeConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
