from api.social_manager.social_recon.constants.platform_constants import MyinstantsConstants

constants = MyinstantsConstants

ROUTES = (
    ("profile/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
