from api.social_manager.social_recon.constants.platform_constants import FreelancehuntConstants

constants = FreelancehuntConstants

ROUTES = (
    (r"freelancer/(?P<id>[^/]+?)\.html", "profile"),
)
