from api.social_manager.social_recon.constants.platform_constants import WarriorForumConstants

constants = WarriorForumConstants

ROUTES = (
    (r"members/(?P<id>[^/]+?)\.html", "profile"),
)
