from api.social_manager.social_recon.constants.platform_constants import ObservableConstants

constants = ObservableConstants

ROUTES = (
    ("@(?P<id>[^/]+?)(?:/.*)?", "profile"),
)
