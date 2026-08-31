from api.social_manager.social_recon.constants.platform_constants import ThelionConstants

constants = ThelionConstants

ROUTES = (
    (r"bin/profile\.cgi\?(?:.*&)?ru_name=(?P<id>[^&]+)(?:&.*)?", "profile"),
)
