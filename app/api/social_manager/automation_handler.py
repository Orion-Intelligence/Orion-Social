import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from typing import Any

import httpx

from api.orion.request_manager.progress_controller import progress_controller

AUTOMATION_CWD = "/app/social-automation"
AD_DETECTION_SCRIPTS = {
    "x": "social:detect-ads",
    "instagram": "social:detect-ig-ads",
}


class automation_handler:
    def __init__(self) -> None:
        self._progress = progress_controller.get_instance()

    def run_post(self, data: dict, job_id: str) -> dict:
        session_state = data.get("session_state")
        platform = str(data.get("platform") or "").strip()
        text = str(data.get("text") or "").strip()
        image_url = str(data.get("image_url") or "").strip()

        session_file = self._write_session_file(session_state)
        result_file = self._new_result_file()
        temp_files = [session_file, result_file]

        cmd_args = [
            "run", "social:post", "--",
            "--session-file", session_file,
            "--platform", platform,
            "--text", text,
            "--result-file", result_file,
        ]

        if image_url:
            image_file = self._download_image(image_url)
            if image_file:
                temp_files.append(image_file)
                cmd_args.extend(["--image", image_file])

        try:
            self._run_automation(cmd_args, job_id)
            return self._build_result(result_file, "post", data)
        finally:
            self._cleanup(temp_files)

    def run_ad_detection(self, data: dict, job_id: str) -> dict:
        session_state = data.get("session_state")
        platform = str(data.get("platform") or "").strip().lower()

        script = AD_DETECTION_SCRIPTS.get(platform)
        if script is None:
            raise ValueError(f"Ad detection is not supported for platform '{platform}'")

        session_file = self._write_session_file(session_state)
        result_file = self._new_result_file()

        cmd_args = [
            "run", script, "--",
            "--session-file", session_file,
            "--result-file", result_file,
        ]

        try:
            self._run_automation(cmd_args, job_id)
            return self._build_result(result_file, "ad_detection", data)
        finally:
            self._cleanup([session_file, result_file])

    def _run_automation(self, cmd_args: list, job_id: str) -> None:
        self._progress.update(job_id, 10, "starting automation")

        process = subprocess.Popen(["npm", *cmd_args], cwd=AUTOMATION_CWD, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        progress = 10
        for line in process.stdout:
            line = line.rstrip()
            print(line, flush=True)
            if line.startswith("["):
                progress = min(90, progress + 1)
                self._progress.update(job_id, progress, line[:80])

        process.wait()
        print(f"[Automation] Process finished (exit={process.returncode})", flush=True)

    def _build_result(self, result_file: str, result_type: str, data: dict) -> dict:
        user_id = str(data.get("user_id") or "")
        profile_id = str(data.get("profile_id") or "")

        with open(result_file, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

        payload["profile_id"] = profile_id
        payload["date_time"] = datetime.now(timezone.utc).isoformat()

        result = {"user_id": user_id, "profile_id": profile_id, "result_type": result_type}
        if result_type == "post":
            result["post_result"] = payload
        else:
            result["ad_detection_result"] = payload
        return result

    @staticmethod
    def _write_session_file(session_state: Any) -> str:
        session_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w")
        json.dump(session_state, session_file)
        session_file.close()
        return session_file.name

    @staticmethod
    def _new_result_file() -> str:
        result_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        result_file.close()
        return result_file.name

    @staticmethod
    def _download_image(image_url: str) -> str:
        image_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        image_file.close()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            with httpx.Client(follow_redirects=True, headers=headers) as client:
                response = client.get(image_url, timeout=15.0)
            if response.status_code != 200:
                print(f"[Automation] Failed to download image {image_url}, status {response.status_code}", flush=True)
                os.unlink(image_file.name)
                return ""
            with open(image_file.name, "wb") as handle:
                handle.write(response.content)
            return image_file.name
        except Exception as exc:
            print(f"[Automation] Failed to download image {image_url}: {exc}", flush=True)
            return ""

    @staticmethod
    def _cleanup(paths: list) -> None:
        for path in paths:
            try:
                if path and os.path.exists(path):
                    os.unlink(path)
            except OSError:
                pass
