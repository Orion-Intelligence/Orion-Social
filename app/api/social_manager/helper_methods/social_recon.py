import json
import os
import re
import shutil
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

    def run_holehe(self, email: str):
        if not shutil.which("holehe"):
            return None
        result = subprocess.run(["holehe", email], capture_output=True, text=True)
        found = []
        for line in result.stdout.splitlines():
            line = line.strip()
            m = re.match(r"^\[\+\]\s*([^:]+):\s*(.+)$", line)
            if m:
                found.append({"service": m.group(1).strip(), "result": m.group(2).strip()})
            elif "found" in line.lower() or line.startswith("[+]"):
                found.append({"line": line})
        return {"returncode": result.returncode, "found": found}

    def parse_username(self, username: str, mode: str = "default", job_id: str | None = None):
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
                raw = self.run_maigret_on_platform(uname, plat)
                if isinstance(raw, dict):
                    k = next((kk for kk in raw.keys() if kk.lower() == plat_lower), None)
                    if k is not None:
                        data = raw[k]
                    elif len(raw) == 1:
                        data = next(iter(raw.values()))
                    else:
                        data = raw
                else:
                    data = raw

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            results.append(
                {
                    "metadata": {
                        "platform": plat,
                        "username": uname,
                        "social_handle": uname,
                        "url": p.get("url"),
                        "timestamp": timestamp,
                    },
                    "data": data,
                }
            )

            if job_id:
                self._progress.update(job_id, int((done / total) * 90), f"done:{plat}:{uname}")

        if job_id:
            self._progress.update(job_id, 95, "finalizing")

        return results

    def parse_email(self, email: str, mode: str = "default", job_id: str | None = None):
        email = (email or "").strip().lower()

        if job_id:
            self._progress.update(job_id, 5, "email:holehe")

        holehe_data = self.run_holehe(email)
        pivot_username = None
        if holehe_data:
            for item in holehe_data.get("found") or []:
                if item:
                    url = item.get("result") or ""
                    m = re.search(r"gravatar\.com/([^/?#\s]+)", url)
                    if m:
                        pivot_username = m.group(1).strip().lower()
                        break
                    srv = item.get("service") or ""
                    m = re.search(r"FullName\s+([^\s/]+)", srv)
                    if m:
                        pivot_username = m.group(1).strip().lower()
                        break

        if not pivot_username and "@" in email:
            pivot_username = email.split("@", 1)[0].strip().lower() or None

        pivot_results = None
        if pivot_username:
            try:
                pivot_results = self.parse_username(pivot_username, mode=mode, job_id=None)
            except Exception:
                pivot_results = None

        if pivot_results:
            for r in pivot_results:
                d = r["data"]
                if d and len(d) == 1:
                    r["data"] = next(iter(d.values()))

        if job_id:
            self._progress.update(job_id, 95, "finalizing")

        return pivot_results

    def parse_phone(self, phone: str, mode: str = "default", job_id: str | None = None):
        p = (phone or "").strip()

        if job_id:
            self._progress.update(job_id, 5, "phone:scan")

        rc = 127
        out = ""
        err = ""
        cmd = []

        if shutil.which("phoneinfoga"):
            cmd = ["phoneinfoga", "scan", "--number", p]
            r = subprocess.run(cmd, capture_output=True, text=True)
            rc = r.returncode
            out = (r.stdout or "").strip()
            err = (r.stderr or "").strip()
            out = re.sub(r"\x1b\[[0-9;]*m", "", out).strip()
            err = re.sub(r"\x1b\[[0-9;]*m", "", err).strip()

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

        parsed = {
            "number": p,
            "country": None,
            "formats": {},
            "urls": [],
            "data": [],
        }

        for line in out.splitlines():
            s = line.strip()
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
                parsed["data"].append(s)

        seen = set()
        urls_dedup = []
        for u in parsed["urls"]:
            if u not in seen:
                seen.add(u)
                urls_dedup.append(u)
        parsed["urls"] = urls_dedup

        if job_id:
            self._progress.update(job_id, 95, "finalizing")

        return {"result": parsed}

    def parse(self, value: str, mode: str = "default", job_id: str | None = None):
        v = (value or "").strip()
        if not v:
            return []

        is_email = "@" in v and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v) is not None
        if is_email:
            return self.parse_email(v, mode=mode, job_id=job_id)

        digits = re.sub(r"\D+", "", v)
        is_phone = re.match(r"^\+?[\d\s().\-]{7,}$", v) is not None and len(digits) >= 7
        if is_phone:
            return self.parse_phone(v, mode=mode, job_id=job_id)

        return self.parse_username(v, mode=mode, job_id=job_id)


if __name__ == "__main__":
    recon = social_recon()
    data = "msmannan00"
    results = recon.parse(data, mode="default", job_id=None)
    print(json.dumps(results, indent=2, ensure_ascii=False))
