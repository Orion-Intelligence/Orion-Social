from api.social_manager.social_recon.constants.platform_constants import CSSBattleConstants

constants = CSSBattleConstants

ROUTES = (
    ("player/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
