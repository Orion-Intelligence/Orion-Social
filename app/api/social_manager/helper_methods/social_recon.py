import json
import os
import re
import subprocess
import time

from api.progress_controller import progress_controller
from api.social_manager.social_enums import SITE_DATA


class social_recon:
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

    def _clean_maigret(self, data: dict) -> dict:
        out = {}
        for site_name, v in (data or {}).items():
            status = (v or {}).get("status") or {}
            ids = status.get("ids") or {}
            tags = status.get("tags") or (v or {}).get("tags") or []
            item = {
                "url": status.get("url") or (v or {}).get("url_user"),
                "status": status.get("status"),
            }
            if ids:
                item["ids"] = ids
            if tags:
                item["tags"] = tags
            if (v or {}).get("http_status") is not None:
                item["http_status"] = (v or {}).get("http_status")
            out[site_name] = item
        return out

    def run_maigret_on_platform(self, username: str, platform: str):
        report_dir = f"reports_{username}"
        os.makedirs(report_dir, exist_ok=True)
        report_file = os.path.join(report_dir, f"report_{username}_simple.json")

        result = subprocess.run(
            ["maigret", username, "--site", platform, "--json", "simple", "--folderoutput", report_dir],
            capture_output=True,
            text=True,
        )

        cleaned = None
        if result.returncode == 0 and os.path.exists(report_file):
            with open(report_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            cleaned = self._clean_maigret(data)
            os.remove(report_file)

        if os.path.exists(report_dir) and not os.listdir(report_dir):
            os.rmdir(report_dir)

        return cleaned

    def run_sherlock(self, username: str):
        cmd = [
            "sherlock",
            username,
            "--timeout", "15",
            "--print-found",
            "--no-color",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        txt_file = f"{username}.txt"
        if os.path.exists(txt_file):
            os.remove(txt_file)

        profiles = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("[+]"):
                match = re.search(r"https?://\S+", line)
                if match:
                    url = match.group(0).rstrip("/")
                    domain = url.split("/")[2].replace("www.", "")
                    platform = domain.split(".")[0].capitalize()
                    user_match = re.search(r"/([^/]+?)(?:/)?$", url)
                    user = user_match.group(1) if user_match else username
                    profiles.append({"platform": platform, "username": user, "url": url})

        return profiles

    def parse(self, username: str, mode: str = "default", job_id: str | None = None):
        if job_id:
            self._progress.update(job_id, 5, "sherlock")

        found_profiles = self.run_sherlock(username)

        total = len(found_profiles) or 1

        seen = set()
        results = []
        done = 0

        focused_lower = {s.lower() for s in SITE_DATA.FOCUSED_SITES}

        for p in found_profiles:
            done += 1
            uname = p["username"].lower()
            plat = p["platform"]
            plat_lower = plat.lower()
            key = (uname, plat)

            if key in seen:
                if job_id:
                    self._progress.update(job_id, int((done / total) * 100), f"skip:{plat}:{uname}")
                continue
            seen.add(key)

            data = None
            if plat_lower in focused_lower:
                if job_id:
                    self._progress.update(job_id, int((done / total) * 90), f"maigret:{plat}:{uname}")
                data = self.run_maigret_on_platform(uname, plat)

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            results.append(
                {
                    "platform": plat,
                    "username": uname,
                    "social_handle": uname,
                    "url": p.get("url"),
                    "timestamp": timestamp,
                    "data": data,
                }
            )

            if job_id:
                self._progress.update(job_id, int((done / total) * 90), f"done:{plat}:{uname}")

        if job_id:
            self._progress.update(job_id, 95, "finalizing")

        return results


if __name__ == "__main__":
    recon = social_recon()
    username = "grok"
    results = recon.parse(username, mode="default", job_id=None)
    print(json.dumps(results, indent=2, ensure_ascii=False))