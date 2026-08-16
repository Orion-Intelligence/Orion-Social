from api.social_manager.social_recon.constants.platform_constants import TVTropesConstants

constants = TVTropesConstants

ROUTES = (
    (r"pmwiki/pmwiki\.php/Tropers/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
