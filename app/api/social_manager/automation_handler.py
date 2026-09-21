import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from typing import Any

import httpx

from api.orion.request_manager.progress_controller import progress_controller

AUTOMATION_CWD = "/app/social-automation"
AD_DETECTION_PLATFORMS = {"x", "instagram", "facebook", "reddit", "pinterest", "youtube", "tiktok", "threads", "quora", "okru", "patreon", "hashnode", "behance", "linkedin", "mewe"}
AD_DETECTION_SCRIPTS = {platform: "social:detect-ads" for platform in AD_DETECTION_PLATFORMS}
HATE_SPEECH_PLATFORMS = {"x", "instagram", "facebook", "reddit", "pinterest", "youtube", "tiktok", "threads", "quora", "okru", "patreon", "hashnode", "behance", "linkedin", "mewe"}
HATE_SPEECH_SCRIPTS = {platform: "social:hate-speech" for platform in HATE_SPEECH_PLATFORMS}
IMAGE_REQUIRED_PLATFORMS = {"instagram", "tiktok", "pinterest", "behance"}
GENERIC_POST_IMAGE = os.path.join(AUTOMATION_CWD, "assets", "generic-post.jpg")


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

        if platform.lower() in IMAGE_REQUIRED_PLATFORMS:
            generic_image = self._generic_image()
            if generic_image:
                cmd_args.extend(["--image", generic_image])
        elif image_url:
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
            "--platform", platform,
            "--session-file", session_file,
            "--result-file", result_file,
        ]

        try:
            self._run_automation(cmd_args, job_id)
            return self._build_result(result_file, "ad_detection", data)
        finally:
            self._cleanup([session_file, result_file])

    def run_hate_speech_monitor(self, data: dict, job_id: str) -> dict:
        session_state = data.get("session_state")
        platform = str(data.get("platform") or "").strip().lower()
        profile_url = str(data.get("profile_url") or "").strip()
        post_count = str(data.get("post_count") or "50")

        script = HATE_SPEECH_SCRIPTS.get(platform)
        if script is None:
            raise ValueError(f"Hate speech monitoring is not supported for platform '{platform}'")

        session_file = self._write_session_file(session_state)
        result_file = self._new_result_file()

        cmd_args = [
            "run", script, "--",
            "--platform", platform,
            "--profile-url", profile_url,
            "--post-count", post_count,
            "--session-file", session_file,
            "--result-file", result_file,
        ]

        try:
            self._run_automation(cmd_args, job_id)
            return self._build_result(result_file, "hate_speech", data)
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
        payload["is_manual"] = data.get("is_manual", False)

        result = {"user_id": user_id, "profile_id": profile_id, "result_type": result_type}
        if result_type == "post":
            result["post_result"] = payload
        elif result_type == "ad_detection":
            if "ads" in payload and isinstance(payload["ads"], list):
                payload["ads"] = payload["ads"][:8]
                payload["total_detected_ads"] = len(payload["ads"])
                try:
                    from api.orion.services.shared.ad_detection_classifier import ad_detection_classifier
                    for ad in payload["ads"]:
                        content_text = ad.get("content_text") or ""
                        if content_text.strip():
                            class_result = ad_detection_classifier.classify(content_text)
                            ad["topic"] = class_result.topic
                        else:
                            ad["topic"] = "Unknown"
                except Exception as e:
                    print(f"[Automation] Error classifying ads: {e}", flush=True)
                    for ad in payload["ads"]:
                        if "topic" not in ad:
                            ad["topic"] = "Unknown"
                            
            result["ad_detection_result"] = payload
        elif result_type == "hate_speech":
            if "posts" in payload and isinstance(payload["posts"], list):
                try:
                    from api.orion.services.shared.hate_speech_classifier import hate_speech_classifier
                    for post in payload["posts"]:
                        content_text = post.get("content_text") or ""
                        if content_text.strip():
                            class_result = hate_speech_classifier.classify(content_text)
                            post["is_hate_speech"] = class_result.is_hate_speech
                            post["label"] = class_result.label
                        else:
                            post["is_hate_speech"] = False
                            post["label"] = "safe"
                except Exception as e:
                    print(f"[Automation] Error classifying hate speech: {e}", flush=True)
                    for post in payload["posts"]:
                        if "is_hate_speech" not in post:
                            post["is_hate_speech"] = False
                            post["label"] = "unknown"
                
                payload["hate_posts_count"] = sum(1 for p in payload.get("posts", []) if p.get("is_hate_speech"))
                
            result["hate_speech_result"] = payload
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
    def _generic_image() -> str:
        return GENERIC_POST_IMAGE if os.path.exists(GENERIC_POST_IMAGE) else ""

    @staticmethod
    def _download_image(image_url: str) -> str:
        urls = [image_url]
        if image_url and "picsum.photos" not in image_url:
            urls.append("https://picsum.photos/640/480")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        for url in urls:
            for attempt in range(3):
                image_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                image_file.close()
                try:
                    with httpx.Client(follow_redirects=True, headers=headers) as client:
                        response = client.get(url, timeout=30.0)
                    if response.status_code == 200 and response.content:
                        with open(image_file.name, "wb") as handle:
                            handle.write(response.content)
                        return image_file.name
                    os.unlink(image_file.name)
                    print(f"[Automation] Image download {url} status {response.status_code} (attempt {attempt + 1})", flush=True)
                except Exception as exc:
                    try:
                        os.unlink(image_file.name)
                    except OSError:
                        pass
                    print(f"[Automation] Image download {url} failed (attempt {attempt + 1}): {exc}", flush=True)
        return ""

    @staticmethod
    def _cleanup(paths: list) -> None:
        for path in paths:
            try:
                if path and os.path.exists(path):
                    os.unlink(path)
            except OSError:
                pass
