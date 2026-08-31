from api.social_manager.social_recon.constants.platform_constants import TemplateMonsterConstants

constants = TemplateMonsterConstants

ROUTES = (
    ("authors/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
