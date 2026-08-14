import re
import subprocess

from api.social_manager.social_recon.constants.extractor_constants import EmailExtractorConstants


class email_extractor:
    @staticmethod
    def extract(email: str) -> dict | None:
        try:
            result = subprocess.run(
                ["holehe", email],
                capture_output=True,
                text=True,
                timeout=EmailExtractorConstants.HOLEHE_TIMEOUT,
            )
        except Exception:
            return None

        found = []
        for line in (result.stdout or "").splitlines():
            match = re.match(r"^\[\+\]\s*([^:]+):\s*(.+)$", line.strip())
            if match:
                found.append(
                    {
                        "service": match.group(1).strip(),
                        "result": match.group(2).strip(),
                    }
                )

        return {"found": found}
