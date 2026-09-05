import asyncio
import hashlib
import hmac
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, BackgroundTasks

from api.orion.model.social_request_model import DuckDuckGoImagesRequest, DuckDuckGoMetadataRequest, DuckDuckGoUsernamesRequest, HateSpeechRequest, SocialReconRequest
from api.orion.services.shared.hate_speech_classifier import HateSpeechResult, hate_speech_classifier
from api.orion.services.shared.env_handler import env_handler
from api.orion.services.shared.request_context_helper import request_context_helper
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class SocialRoutes:
    def __init__(self, orion: Any) -> None:
        self.orion = orion
        self.router = APIRouter(dependencies=[Depends(self.require_internal_request)])
        self.router.add_api_route("/social/recon", self.social_recon, methods=["POST"])
        self.router.add_api_route("/social/recon/image", self.social_recon_image, methods=["POST"])
        self.router.add_api_route("/social/online/usernames", self.online_usernames, methods=["POST"])
        self.router.add_api_route("/social/online/images", self.online_images, methods=["POST"])
        self.router.add_api_route("/social/metadata", self.metadata, methods=["POST"])
        self.router.add_api_route("/social/hate-speech", self.classify_hate_speech, methods=["POST"], response_model=HateSpeechResult)
        self.router.add_api_route("/social/automation/post", self.trigger_post, methods=["POST"])
        self.router.add_api_route("/social/automation/ad-monitor", self.trigger_ad_monitor, methods=["POST"])

    async def run_background_automation(self, cmd_args: list, callback_url: str, token: str, result_file: str = "", result_type: str = "", user_id: str = "", profile_id: str = "", files_to_cleanup: list = None):
        import asyncio
        import httpx
        try:
            process = await asyncio.create_subprocess_exec(
                "npm", *cmd_args,
                cwd="/app/social-automation",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            # Streamed rather than communicate() so the automation's own prints reach
            # the container log live instead of only after the process exits. Lines are
            # still collected for the callback's output/error fields.
            out_lines, err_lines = [], []

            async def drain(stream, sink):
                async for raw in stream:
                    text = raw.decode('utf-8', errors='replace').rstrip()
                    print(text, flush=True)
                    sink.append(text)

            await asyncio.gather(drain(process.stdout, out_lines), drain(process.stderr, err_lines))
            await process.wait()

            output = "\n".join(out_lines)
            error = "\n".join(err_lines)

            print(f"[Automation] Process finished (exit={process.returncode})", flush=True)
            result = self.read_automation_result(result_file, result_type, user_id, profile_id)
            print(f"[Automation] Structured result: {'parsed' if result else 'MISSING'}", flush=True)

            if callback_url:
                headers = {"x-orion-internal-token": token} if token else {}
                print(f"[Automation] Sending callback to {callback_url}", flush=True)
                async with httpx.AsyncClient() as client:
                    response = await client.post(callback_url, json={"status": "complete", "output": output, "error": error, "result": result}, headers=headers, timeout=10.0)
                print(f"[Automation] Callback response: {response.status_code}", flush=True)
        except Exception as e:
            print(f"[Automation] Run failed: {type(e).__name__}: {e}", flush=True)
            result = self.read_automation_result(result_file, result_type, user_id, profile_id)
            if callback_url:
                headers = {"x-orion-internal-token": token} if token else {}
                try:
                    print(f"[Automation] Sending failure callback to {callback_url}", flush=True)
                    async with httpx.AsyncClient() as client:
                        await client.post(callback_url, json={"status": "failed", "error": str(e), "result": result}, headers=headers, timeout=10.0)
                except Exception as callback_error:
                    print(f"[Automation] Failure callback could not be sent: {callback_error}", flush=True)
        finally:
            if files_to_cleanup:
                import os
                for f in files_to_cleanup:
                    try:
                        if os.path.exists(f):
                            os.unlink(f)
                    except OSError:
                        pass

    def read_automation_result(self, result_file: str, result_type: str, user_id: str, profile_id: str):
        import json
        import os
        from datetime import datetime, timezone

        if not result_file or not result_type:
            return None

        try:
            with open(result_file, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as read_error:
            print(f"[Automation] Could not read result file {result_file}: {read_error}")
            return None
        finally:
            try:
                os.unlink(result_file)
            except OSError:
                pass

        data["profile_id"] = profile_id
        data["date_time"] = datetime.now(timezone.utc).isoformat()

        result = {"user_id": user_id, "profile_id": profile_id, "result_type": result_type}
        if result_type == "post":
            result["post_result"] = data
        else:
            result["ad_detection_result"] = data
        return result

    async def require_internal_request(self, request: Request) -> None:
        expected = env_handler.get_instance().env("ORION_SOCIAL_INTERNAL_TOKEN", "").strip()
        provided = request.headers.get("x-orion-internal-token", "")
        if not expected or not hmac.compare_digest(provided, expected):
            raise HTTPException(status_code=403, detail="forbidden")

    async def social_recon(self, request: Request, payload: SocialReconRequest) -> Any:
        context_key = request_context_helper.context_key(request)
        job_id = str(hash(f"recon:{context_key}:{payload.query}:default"))
        data = request_context_helper.with_request_context({"job_id": job_id, "username": payload.query, "mode": "default"}, request)
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_USER, data)

    async def social_recon_image(self, request: Request, file: UploadFile = File(...)) -> Any:
        content = await file.read()
        content_hash = hashlib.sha256(content or b"").hexdigest()
        job_id = f"recon_image:{request_context_helper.context_key(request)}:{content_hash}"
        data = request_context_helper.with_request_context({"job_id": job_id, "filename": file.filename or "", "file_bytes": content}, request)
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_IMAGE, data)

    async def online_usernames(self, request: Request, payload: DuckDuckGoUsernamesRequest) -> Any:
        platform = payload.platform or ""
        job_id = str(hash(f"ddg_usernames:{request_context_helper.context_key(request)}:{platform}:{payload.username}"))
        data = request_context_helper.with_request_context({"job_id": job_id, "platform": platform, "username": payload.username}, request)
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_USERNAMES, data)

    async def online_images(self, request: Request, payload: DuckDuckGoImagesRequest) -> Any:
        platform = payload.platform or ""
        username = payload.username or ""
        hash_id = payload.hash_id or ""
        job_id = str(hash(f"ddg_images:{request_context_helper.context_key(request)}:{platform}:{username}:{payload.max_images}:{hash_id}"))
        data = request_context_helper.with_request_context({"job_id": job_id, "platform": platform, "username": username, "max_images": payload.max_images, "hash_id": hash_id}, request)
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES, data)

    async def metadata(self, request: Request, payload: DuckDuckGoMetadataRequest) -> Any:
        platform = payload.platform or ""
        username = payload.username or ""
        job_id = str(hash(f"ddg_metadata:{request_context_helper.context_key(request)}:{platform}:{username}:{payload.tokens}"))
        data = request_context_helper.with_request_context({"job_id": job_id, "platform": platform, "username": username, "tokens": payload.tokens}, request)
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_METADATA, data)

    async def classify_hate_speech(self, payload: HateSpeechRequest) -> HateSpeechResult:
        return await asyncio.to_thread(hate_speech_classifier.classify, payload.text)

    async def trigger_post(self, request: Request, background_tasks: BackgroundTasks) -> Any:
        import tempfile
        import json
        import httpx
        
        data = await request.json()
        session_state = data.get("session_state")
        platform = data.get("platform")
        text = data.get("text")
        image_url = data.get("image_url")
        callback_url = data.get("callback_url")
        user_id = data.get("user_id") or ""
        profile_id = data.get("profile_id") or ""
        token = request.headers.get("x-orion-internal-token", "")
        
        if not session_state or not platform or not text:
            raise HTTPException(status_code=400, detail="session_state, platform, and text are required")
            
        session_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w')
        json.dump(session_state, session_file)
        session_file.close()

        result_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        result_file.close()
        
        files_to_cleanup = [session_file.name, result_file.name]
        cmd_args = ["run", "social:post", "--", "--session-file", session_file.name, "--platform", platform, "--text", text, "--result-file", result_file.name]
        
        if image_url:
            image_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            image_file.close()
            files_to_cleanup.append(image_file.name)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
                img_resp = await client.get(image_url, timeout=15.0)
                if img_resp.status_code == 200:
                    with open(image_file.name, 'wb') as f:
                        f.write(img_resp.content)
                    cmd_args.extend(["--image", image_file.name])
                else:
                    import logging
                    logging.error(f"Failed to download image {image_url}, status code: {img_resp.status_code}")
                    
        background_tasks.add_task(self.run_background_automation, cmd_args, callback_url, token, result_file.name, "post", user_id, profile_id, files_to_cleanup)
        return {"status": "started"}

    async def trigger_ad_monitor(self, request: Request, background_tasks: BackgroundTasks) -> Any:
        import tempfile
        import json
        
        data = await request.json()
        session_state = data.get("session_state")
        platform = data.get("platform")
        callback_url = data.get("callback_url")
        user_id = data.get("user_id") or ""
        profile_id = data.get("profile_id") or ""
        token = request.headers.get("x-orion-internal-token", "")

        if not session_state or not platform:
            raise HTTPException(status_code=400, detail="session_state and platform are required")
            
        session_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w')
        json.dump(session_state, session_file)
        session_file.close()

        result_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        result_file.close()
        
        files_to_cleanup = [session_file.name, result_file.name]
        script = "social:detect-ig-ads" if platform == "instagram" else "social:detect-ads"
        cmd_args = ["run", script, "--", "--session-file", session_file.name, "--result-file", result_file.name]
        
        background_tasks.add_task(self.run_background_automation, cmd_args, callback_url, token, result_file.name, "ad_detection", user_id, profile_id, files_to_cleanup)
        return {"status": "started"}
