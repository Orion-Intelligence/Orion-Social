import re
import shutil
import subprocess
import time

from api.orion.request_manager.progress_controller import progress_controller


class phone_recon:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self._progress = progress_controller.get_instance()

    def parse_phone(self, phone: str, mode: str = "default", job_id: str | None = None):
        p = (phone or "").strip()

        if job_id:
            self._progress.update(job_id, 2, "init:phone")

        if job_id:
            self._progress.update(job_id, 5, "phone:scan")

        rc = 127
        out = ""
        err = ""
        cmd = []

        if shutil.which("phoneinfoga"):
            cmd = ["phoneinfoga", "scan", "--number", p]
            if job_id:
                self._progress.update(job_id, 10, "phoneinfoga:run")
            r = subprocess.run(cmd, capture_output=True, text=True)
            rc = r.returncode
            out = (r.stdout or "").strip()
            err = (r.stderr or "").strip()
            out = re.sub(r"\x1b\[[0-9;]*m", "", out).strip()
            err = re.sub(r"\x1b\[[0-9;]*m", "", err).strip()
            if job_id:
                self._progress.update(job_id, 35, f"phoneinfoga:exit:{rc}")

        if rc != 0:
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if job_id:
                self._progress.update(job_id, 95, "finalizing")
            return {
                "result": {
                    "phone": p,
                    "timestamp": ts,
                    "status": {"code": rc},
                    "results": {"error": err or out or "phoneinfoga not available"},
                    "debug": {"cmd": " ".join(cmd)},
                    "data": [],
                }
            }

        if job_id:
            self._progress.update(job_id, 50, "phone:parse")

        parsed = {
            "number": p,
            "country": None,
            "formats": {},
            "details": {},
            "urls": [],
            "data": [],
        }

        lines = out.splitlines()
        total_lines = len(lines) or 1
        for i, line in enumerate(lines, start=1):
            s = line.strip()
            if job_id and (i == 1 or i == total_lines or i % 25 == 0):
                self._progress.update(job_id, 50, f"phone:parse:{i}/{total_lines}")
            if not s:
                continue
            if s.startswith("Country:"):
                parsed["country"] = s.split(":", 1)[1].strip()
            elif s.startswith("E164:"):
                parsed["formats"]["e164"] = s.split(":", 1)[1].strip()
            elif s.startswith("International:"):
                parsed["formats"]["international"] = s.split(":", 1)[1].strip()
            elif s.startswith("Local:"):
                parsed["formats"]["local"] = s.split(":", 1)[1].strip()
            elif "URL:" in s:
                parsed["urls"].append(s.split("URL:", 1)[1].strip())
            elif ":" in s and not s.endswith(":"):
                key, value = s.split(":", 1)
                key = key.strip()
                value = value.strip()
                if not value:
                    continue
                if key.lower() in {"country", "e164", "international", "local"}:
                    continue
                if key.lower() == "raw local":
                    parsed["data"].append(s)
                    continue
                existing = parsed["details"].get(key)
                if existing is None:
                    parsed["details"][key] = value
                elif isinstance(existing, list):
                    if value not in existing:
                        existing.append(value)
                elif existing != value:
                    parsed["details"][key] = [existing, value]

        if job_id:
            self._progress.update(job_id, 75, "phone:dedup")

        seen = set()
        urls_dedup = []
        for u in parsed["urls"]:
            if u not in seen:
                seen.add(u)
                urls_dedup.append(u)
        parsed["urls"] = urls_dedup

        if job_id:
            self._progress.update(job_id, 95, "finalizing")

        parsed.pop("urls", None)
        return {"result": parsed}
