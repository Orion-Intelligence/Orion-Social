from api.social_manager.social_recon.constants.platform_constants import TrueAchievementsConstants

constants = TrueAchievementsConstants

ROUTES = (
    ("gamer/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
