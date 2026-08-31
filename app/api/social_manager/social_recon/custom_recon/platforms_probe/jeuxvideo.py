from api.social_manager.social_recon.constants.platform_constants import JeuxVideoConstants

constants = JeuxVideoConstants

ROUTES = (
    ("profil/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
