from api.social_manager.social_recon.constants.platform_constants import WikidotConstants

constants = WikidotConstants

ROUTES = (
    ("user:info/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
