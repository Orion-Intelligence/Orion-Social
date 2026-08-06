import hashlib
import hmac
import os

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from api.orion.services.shared.env_handler import env_handler
from api.orion.model.social_request_model import SocialReconRequest, SocialPhoneReconRequest, SocialProfileRequest, SocialFollowersRequest, SocialFollowingRequest, SocialPostsRequest, SocialVideosRequest, SocialShortsRequest, DuckDuckGoUsernamesRequest, DuckDuckGoImagesRequest, DuckDuckGoMetadataRequest
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class SocialRoutes:
    def __init__(self, orion):
        self.orion = orion
        self.router = APIRouter(dependencies=[Depends(self.require_internal_request)])
        self.router.add_api_route("/social/recon", self.social_recon, methods=["POST"])
        self.router.add_api_route("/social/phone", self.phone_recon, methods=["POST"])
        self.router.add_api_route("/social/recon/image", self.social_recon_image, methods=["POST"])
        self.router.add_api_route("/social/profile", self.social_profile, methods=["POST"])
        self.router.add_api_route("/social/followers", self.social_followers, methods=["POST"])
        self.router.add_api_route("/social/following", self.social_following, methods=["POST"])
        self.router.add_api_route("/social/posts", self.social_posts, methods=["POST"])
        self.router.add_api_route("/social/videos", self.social_videos, methods=["POST"])
        self.router.add_api_route("/social/shorts", self.social_shorts, methods=["POST"])
        self.router.add_api_route("/social/online/usernames", self.online_usernames, methods=["POST"])
        self.router.add_api_route("/social/online/images", self.online_images, methods=["POST"])
        self.router.add_api_route("/social/metadata", self.metadata, methods=["POST"])

    async def require_internal_request(self, request: Request):
        expected = env_handler.get_instance().env("ORION_SOCIAL_INTERNAL_TOKEN", "").strip()
        provided = request.headers.get("x-orion-internal-token", "")
        if not expected or not hmac.compare_digest(provided, expected):
            raise HTTPException(status_code=403, detail="forbidden")
        
    @staticmethod
    def _header(request: Request, name: str) -> str:
        return str(request.headers.get(name, "") or "").strip()

    def _context_key(self, request: Request) -> str:
        username = self._header(request, "x-orion-user")
        user_id = self._header(request, "x-orion-user-id")
        session_id = self._header(request, "x-orion-session-id")
        return hashlib.sha256("|".join([username, user_id, session_id]).encode("utf-8")).hexdigest()

    def _with_request_context(self, data: dict, request: Request) -> dict:
        context = {
            "orion_user": self._header(request, "x-orion-user"),
            "orion_user_id": self._header(request, "x-orion-user-id"),
            "orion_tenant_id": self._header(request, "x-orion-tenant-id"),
            "orion_session_id": self._header(request, "x-orion-session-id"),
            "orion_session_client": self._header(request, "x-orion-session-client") or "web",
        }
        return {**data, **{key: value for key, value in context.items() if value}}

    @staticmethod
    def _field_was_sent(model, field_name: str) -> bool:
        return field_name in getattr(model, "model_fields_set", getattr(model, "__fields_set__", set()))

    async def social_recon(self, request: Request, p: SocialReconRequest):
        context_key = self._context_key(request)
        job_id = str(hash(f"recon:{context_key}:{p.query}:default"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_USER, self._with_request_context({"job_id": job_id, "username": p.query, "mode": "default"}, request))

    async def phone_recon(self, request: Request, p: SocialPhoneReconRequest):
        context_key = self._context_key(request)
        job_id = str(hash(f"recon_phone:{context_key}:{p.query}:default"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_PHONE, self._with_request_context({"job_id": job_id, "phone": p.query, "mode": "default"}, request))

    async def social_recon_image(self, request: Request, file: UploadFile = File(...)):
        content = await file.read()
        content_hash = hashlib.sha256(content or b"").hexdigest()
        job_id = f"recon_image:{self._context_key(request)}:{content_hash}"
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_IMAGE, self._with_request_context({"job_id": job_id, "filename": file.filename or "", "file_bytes": content}, request),)

    async def social_profile(self, request: Request, p: SocialProfileRequest):
        target_type = p.target_type or "profile"
        social_data_type = p.social_data_type or "profile_info"
        executor = "extension" if p.use_extension else "legacy"
        max_posts = 20 if p.use_extension and not self._field_was_sent(p, "max_posts") else p.max_posts
        max_shorts = 20 if p.use_extension and not self._field_was_sent(p, "max_shorts") else p.max_shorts
        job_id = str(hash(f"profile:{self._context_key(request)}:{executor}:{p.platform}:{p.username}:{social_data_type}:{target_type}:{max_posts}:{max_shorts}:{p.max_comments}:{p.max_followers}:{p.max_following}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username, "social_data_type": social_data_type,"target_type": target_type, "use_extension": p.use_extension, "max_posts": max_posts, "max_shorts": max_shorts, "max_comments": p.max_comments, "max_followers": p.max_followers, "max_following": p.max_following}, request))
        
    async def social_followers(self, request: Request, p: SocialFollowersRequest):
        target_type = p.target_type or "profile"
        social_data_type = p.social_data_type or "followers"
        job_id = str(hash(f"followers:{self._context_key(request)}:{p.platform}:{p.username}:{p.max_followers}:{social_data_type}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username, "max_followers": p.max_followers, "social_data_type": social_data_type,"target_type": target_type}, request))
        
    async def social_following(self, request: Request, p: SocialFollowingRequest):
        target_type = p.target_type or "profile"
        social_data_type = p.social_data_type or "following"
        job_id = str(hash(f"following:{self._context_key(request)}:{p.platform}:{p.username}:{p.max_following}:{social_data_type}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username, "max_following": p.max_following, "social_data_type": social_data_type,"target_type": target_type}, request))
        
    async def social_posts(self, request: Request, p: SocialPostsRequest):
        target_type = p.target_type or "profile"
        social_data_type = p.social_data_type or "posts"
        hash_id = p.hash_id or ""
        executor = "extension" if p.use_extension else "legacy"
        max_posts = 20 if p.use_extension and not self._field_was_sent(p, "max_posts") else p.max_posts
        max_comments = 25 if p.use_extension and not self._field_was_sent(p, "max_comments") else p.max_comments
        existing_url_hash = hash(tuple(p.existing_post_urls))
        job_id = str(hash(f"posts:{self._context_key(request)}:{executor}:{p.platform}:{p.username}:{max_posts}:{max_comments}:{p.post_offset}:{p.existing_posts_count}:{existing_url_hash}:{p.comment_offset}:{social_data_type}:{hash_id}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_POSTS, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username, "max_posts": max_posts, "max_comments": max_comments, "post_offset": p.post_offset, "existing_posts_count": p.existing_posts_count, "existing_post_urls": p.existing_post_urls, "comment_offset": p.comment_offset, "social_data_type": social_data_type, "hash_id": hash_id, "target_type": target_type, "use_extension": p.use_extension}, request))
        
    async def social_videos(self, request: Request, p: SocialVideosRequest):
        target_type = p.target_type or "profile"
        social_data_type = p.social_data_type or "videos"
        hash_id = p.hash_id or ""
        executor = "extension" if p.use_extension else "legacy"
        job_id = str(hash(f"videos:{self._context_key(request)}:{executor}:{p.platform}:{p.username}:{p.max_videos}:{p.max_comments}:{p.comment_offset}:{social_data_type}:{hash_id}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_VIDEOS, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username, "max_videos": p.max_videos, "max_comments": p.max_comments, "comment_offset": p.comment_offset, "social_data_type": social_data_type, "hash_id": hash_id, "target_type": target_type, "use_extension": p.use_extension}, request))
        
    async def social_shorts(self, request: Request, p: SocialShortsRequest):
        target_type = p.target_type or "profile"
        social_data_type = p.social_data_type or "shorts"
        hash_id = p.hash_id or ""
        executor = "extension" if p.use_extension else "legacy"
        existing_url_hash = hash(tuple(p.existing_post_urls))
        job_id = str(hash(f"shorts:{self._context_key(request)}:{executor}:{p.platform}:{p.username}:{p.max_shorts}:{p.max_comments}:{p.post_offset}:{p.existing_posts_count}:{existing_url_hash}:{p.comment_offset}:{social_data_type}:{hash_id}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_SHORTS, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username, "max_shorts": p.max_shorts, "max_comments": p.max_comments, "post_offset": p.post_offset, "existing_posts_count": p.existing_posts_count, "existing_post_urls": p.existing_post_urls, "comment_offset": p.comment_offset, "social_data_type": social_data_type, "hash_id": hash_id, "target_type": target_type, "use_extension": p.use_extension}, request))
        
    async def online_usernames(self, request: Request, p: DuckDuckGoUsernamesRequest):
        job_id = str(hash(f"ddg_usernames:{self._context_key(request)}:{p.platform}:{p.username}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_USERNAMES, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username}, request))

    async def online_images(self, request: Request, p: DuckDuckGoImagesRequest):
        hash_id = p.hash_id or ""
        executor = "extension" if p.use_extension else "legacy"
        job_id = str(hash(f"ddg_images:{self._context_key(request)}:{executor}:{p.platform}:{p.username}:{p.max_images}:{hash_id}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username, "max_images": p.max_images, "hash_id": hash_id, "use_extension": p.use_extension}, request))

    async def metadata(self, request: Request, p: DuckDuckGoMetadataRequest):
        job_id = str(hash(f"ddg_metadata:{self._context_key(request)}:{p.platform}:{p.username}:{p.tokens}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_METADATA, self._with_request_context({"job_id": job_id, "platform": p.platform, "username": p.username, "tokens": p.tokens}, request))
