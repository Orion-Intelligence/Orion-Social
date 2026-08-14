import asyncio
import hashlib
import hmac
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

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
