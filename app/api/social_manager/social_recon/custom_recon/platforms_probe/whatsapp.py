from api.social_manager.social_recon.constants.platform_constants import WhatsAppConstants

constants = WhatsAppConstants

HOSTS = ("chat.whatsapp.com",)
ROUTES = (
    (r"(?P<id>\+?\d{7,15})", "profile"),
    ("(?P<id>[A-Za-z0-9]{10,})", "group"),
)
