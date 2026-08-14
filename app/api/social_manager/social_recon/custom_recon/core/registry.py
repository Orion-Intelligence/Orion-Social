from types import ModuleType

import api.social_manager.social_recon.custom_recon.platforms_probe.bluesky as bluesky
import api.social_manager.social_recon.custom_recon.platforms_probe.discord as discord
import api.social_manager.social_recon.custom_recon.platforms_probe.facebook as facebook
import api.social_manager.social_recon.custom_recon.platforms_probe.instagram as instagram
import api.social_manager.social_recon.custom_recon.platforms_probe.linkedin as linkedin
import api.social_manager.social_recon.custom_recon.platforms_probe.pinterest as pinterest
import api.social_manager.social_recon.custom_recon.platforms_probe.quora as quora
import api.social_manager.social_recon.custom_recon.platforms_probe.reddit as reddit
import api.social_manager.social_recon.custom_recon.platforms_probe.snapchat as snapchat
import api.social_manager.social_recon.custom_recon.platforms_probe.threads as threads
import api.social_manager.social_recon.custom_recon.platforms_probe.tiktok as tiktok
import api.social_manager.social_recon.custom_recon.platforms_probe.twitch as twitch
import api.social_manager.social_recon.custom_recon.platforms_probe.whatsapp as whatsapp
import api.social_manager.social_recon.custom_recon.platforms_probe.x as x
import api.social_manager.social_recon.custom_recon.platforms_probe.youtube as youtube
from api.social_manager.social_recon.constants.custom_recon_constants import RegistryConstants

platforms: dict[str, ModuleType] = {
    "facebook": facebook,
    "instagram": instagram,
    "youtube": youtube,
    "tiktok": tiktok,
    "linkedin": linkedin,
    "x": x,
    "reddit": reddit,
    "whatsapp": whatsapp,
    "pinterest": pinterest,
    "snapchat": snapchat,
    "threads": threads,
    "bluesky": bluesky,
    "discord": discord,
    "quora": quora,
    "twitch": twitch,
}


def resolve(name: str) -> ModuleType | None:
    key = (name or "").strip().lower()
    return platforms.get(RegistryConstants.ALIASES.get(key, key))


def supported(module: ModuleType) -> bool:
    return getattr(module.constants, "SUPPORTED", True)


def names() -> tuple[str, ...]:
    return tuple(platforms)
