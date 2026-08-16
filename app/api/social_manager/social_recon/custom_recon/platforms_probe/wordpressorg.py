from api.social_manager.social_recon.constants.platform_constants import WordPressOrgConstants

constants = WordPressOrgConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
