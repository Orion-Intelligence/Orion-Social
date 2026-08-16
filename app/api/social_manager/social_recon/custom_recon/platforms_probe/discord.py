from api.social_manager.social_recon.constants.platform_constants import DiscordConstants

constants = DiscordConstants

HOSTS = ("discord.gg",)
ROUTES = (
    (r"users/(?P<id>\d+)", "profile"),
    ("(?:invite/)?(?P<id>[A-Za-z0-9-]+)", "server"),
)
