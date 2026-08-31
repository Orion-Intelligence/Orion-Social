from api.social_manager.social_recon.constants.platform_constants import DomestikaOrgConstants

constants = DomestikaOrgConstants

ROUTES = (
    ("(?P<id>[^/]+)(?:/.*)?", "profile"),
)
