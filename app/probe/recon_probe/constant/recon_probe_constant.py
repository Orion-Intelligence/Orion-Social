from pathlib import Path


class ReconProbeConstants:
    RECON_PROBE_ROOT = Path(__file__).resolve().parents[1]
    REPOSITORY_ROOT = RECON_PROBE_ROOT.parents[2]
    APPLICATION_ROOT = REPOSITORY_ROOT / "app"
    PLATFORM_ROOT = APPLICATION_ROOT / "api/social_manager/social_recon/custom_recon/platforms_probe"

    PLATFORM_SCRIPT_MODULE = "app.probe.recon_probe.test_platform_probe"
    EMAIL_SCRIPT_MODULE = "app.probe.recon_probe.test_email_probe"
    NAME_SCRIPT_MODULE = "app.probe.recon_probe.test_name_probe"

    PLATFORM_MODULE_PREFIX = "api.social_manager.social_recon.custom_recon.platforms_probe"
    EMAIL_MODULE = "api.social_manager.social_recon.extractors.email_extractor"
    NAME_MODULE = "api.social_manager.social_recon.extractors.username_extractor"
    RESULT_PREFIX = "RECON_PROBE_RESULT="

    SAMPLE_USERNAME = "orionprobe"
    VALID_VERDICTS = {"exists", "absent", "unknown", "unsupported"}
    REQUIRED_PLATFORM_MEMBERS = ("NAME", "PROFILE_URL")
