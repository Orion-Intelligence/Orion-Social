from api.social_manager.social_recon.constants.platform_constants import LomographyConstants

constants = LomographyConstants

ROUTES = (
    ("homes/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
