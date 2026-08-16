from api.social_manager.social_recon.constants.platform_constants import TripAdvisorConstants

constants = TripAdvisorConstants

ROUTES = (
    ("members/(?P<id>[^/]+)(?:/.*)?", "profile"),
)
