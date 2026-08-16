from api.social_manager.social_recon.constants.platform_constants import DeepDreamGeneratorConstants

constants = DeepDreamGeneratorConstants

ROUTES = (
    ("u/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
