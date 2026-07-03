import hashlib

from fastapi import APIRouter, UploadFile, File

from api.orion.model.social_request_model import SocialReconRequest, SocialPhoneReconRequest, SocialProfileRequest, SocialFollowersRequest, SocialFollowingRequest, SocialPostsRequest, SocialVideosRequest, SocialShortsRequest, DuckDuckGoUsernamesRequest, DuckDuckGoImagesRequest, DuckDuckGoMetadataRequest
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class SocialRoutes:
    def __init__(self, orion):
        self.orion = orion
        self.router = APIRouter()
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

    async def social_recon(self, p: SocialReconRequest):
        job_id = str(hash(f"recon:{p.query}:default"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_USER, {"job_id": job_id, "username": p.query, "mode": "default"})

    async def phone_recon(self, p: SocialPhoneReconRequest):
        job_id = str(hash(f"recon_phone:{p.query}:default"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_PHONE, {"job_id": job_id, "phone": p.query, "mode": "default"})

    async def social_recon_image(self, file: UploadFile = File(...)):
        content = await file.read()
        content_hash = hashlib.sha256(content or b"").hexdigest()
        job_id = f"recon_image:{content_hash}"
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_IMAGE, {"job_id": job_id, "filename": file.filename or "", "file_bytes": content},)

    async def social_profile(self, p: SocialProfileRequest):
        social_data_type = p.social_data_type or "profile_info"
        target_type = p.target_type or "profile"
        job_id = str(hash(f"profile:{p.platform}:{p.username}:{social_data_type}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY, {"job_id": job_id, "platform": p.platform, "username": p.username, "social_data_type": social_data_type, "target_type": target_type})

    async def social_followers(self, p: SocialFollowersRequest):
        social_data_type = p.social_data_type or "followers"
        target_type = p.target_type or "profile"
        job_id = str(hash(f"followers:{p.platform}:{p.username}:{p.max_followers}:{social_data_type}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_followers": p.max_followers, "social_data_type": social_data_type, "target_type": target_type})

    async def social_following(self, p: SocialFollowingRequest):
        social_data_type = p.social_data_type or "following"
        target_type = p.target_type or "profile"
        job_id = str(hash(f"following:{p.platform}:{p.username}:{p.max_following}:{social_data_type}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_following": p.max_following, "social_data_type": social_data_type, "target_type": target_type})

    async def social_posts(self, p: SocialPostsRequest):
        social_data_type = p.social_data_type or "posts"
        hash_id = p.hash_id or ""
        target_type = p.target_type or "profile"
        job_id = str(hash(f"posts:{p.platform}:{p.username}:{p.max_posts}:{p.max_comments}:{p.comment_offset}:{social_data_type}:{hash_id}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_POSTS, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_posts": p.max_posts, "max_comments": p.max_comments, "comment_offset": p.comment_offset, "social_data_type": social_data_type, "hash_id": hash_id, "target_type": target_type})

    async def social_videos(self, p: SocialVideosRequest):
        social_data_type = p.social_data_type or "videos"
        hash_id = p.hash_id or ""
        target_type = p.target_type or "profile"
        job_id = str(hash(f"videos:{p.platform}:{p.username}:{p.max_videos}:{p.max_comments}:{p.comment_offset}:{social_data_type}:{hash_id}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_VIDEOS, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_videos": p.max_videos, "max_comments": p.max_comments, "comment_offset": p.comment_offset, "social_data_type": social_data_type, "hash_id": hash_id, "target_type": target_type})

    async def social_shorts(self, p: SocialShortsRequest):
        social_data_type = p.social_data_type or "shorts"
        hash_id = p.hash_id or ""
        target_type = p.target_type or "profile"
        job_id = str(hash(f"shorts:{p.platform}:{p.username}:{p.max_shorts}:{p.max_comments}:{p.comment_offset}:{social_data_type}:{hash_id}:{target_type}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_SHORTS, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_shorts": p.max_shorts, "max_comments": p.max_comments, "comment_offset": p.comment_offset, "social_data_type": social_data_type, "hash_id": hash_id, "target_type": target_type})

    async def online_usernames(self, p: DuckDuckGoUsernamesRequest):
        job_id = str(hash(f"ddg_usernames:{p.platform}:{p.username}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_USERNAMES, {"job_id": job_id, "platform": p.platform, "username": p.username})

    async def online_images(self, p: DuckDuckGoImagesRequest):
        hash_id = p.hash_id or ""
        job_id = str(hash(f"ddg_images:{p.platform}:{p.username}:{p.max_images}:{hash_id}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_images": p.max_images, "hash_id": hash_id})

    async def metadata(self, p: DuckDuckGoMetadataRequest):
        job_id = str(hash(f"ddg_metadata:{p.platform}:{p.username}:{p.tokens}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_METADATA, {"job_id": job_id, "platform": p.platform, "username": p.username, "tokens": p.tokens})
