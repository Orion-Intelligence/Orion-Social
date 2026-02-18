from fastapi import APIRouter

from api.orion.model.social_request_model import SocialReconRequest, SocialScrapeRequest, SocialProfileRequest, SocialFollowersRequest, SocialFollowingRequest, SocialPostsRequest, DuckDuckGoUsernamesRequest, DuckDuckGoImagesRequest, DuckDuckGoMetadataRequest
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class SocialRoutes:
    def __init__(self, orion):
        self.orion = orion
        self.router = APIRouter()
        self.router.add_api_route("/social/recon", self.social_recon, methods=["POST"])
        self.router.add_api_route("/social/scrape", self.social_scrape, methods=["POST"])
        self.router.add_api_route("/social/profile", self.social_profile, methods=["POST"])
        self.router.add_api_route("/social/followers", self.social_followers, methods=["POST"])
        self.router.add_api_route("/social/following", self.social_following, methods=["POST"])
        self.router.add_api_route("/social/posts", self.social_posts, methods=["POST"])
        self.router.add_api_route("/social/duckduckgo/usernames", self.duckduckgo_usernames, methods=["POST"])
        self.router.add_api_route("/social/duckduckgo/images", self.duckduckgo_images, methods=["POST"])
        self.router.add_api_route("/social/metadata", self.metadata, methods=["POST"])


    async def social_recon(self, p: SocialReconRequest):
        job_id = str(hash(f"recon:{p.query}:default"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_RECON_USER, {"job_id": job_id, "username": p.query, "mode": "default"})

    async def social_scrape(self, p: SocialScrapeRequest):
        job_id = str(hash(f"scrape:{p.model_dump()}"))
        targets = [{"platform": t.platform, "usernames": t.usernames, "max_followers": t.max_followers, "max_following": t.max_following} for t in p.targets]
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE, {"job_id": job_id, "scrape_key": job_id, "targets": targets, "compare_results": True, "similarity_threshold": 70})

    async def social_profile(self, p: SocialProfileRequest):
        job_id = str(hash(f"profile:{p.platform}:{p.username}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY, {"job_id": job_id, "platform": p.platform, "username": p.username})

    async def social_followers(self, p: SocialFollowersRequest):
        job_id = str(hash(f"followers:{p.platform}:{p.username}:{p.max_followers}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_followers": p.max_followers})

    async def social_following(self, p: SocialFollowingRequest):
        job_id = str(hash(f"following:{p.platform}:{p.username}:{p.max_following}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_following": p.max_following})

    async def social_posts(self, p: SocialPostsRequest):
        job_id = str(hash(f"posts:{p.platform}:{p.username}:{p.max_posts}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_POSTS, {"job_id": job_id, "platform": p.platform, "username": p.username, "max_posts": p.max_posts})

    async def duckduckgo_usernames(self, p: DuckDuckGoUsernamesRequest):
        job_id = str(hash(f"ddg_usernames:{p.platform}:{p.username}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_USERNAMES, {"job_id": job_id, "platform": p.platform, "username": p.username})

    async def duckduckgo_images(self, p: DuckDuckGoImagesRequest):
        job_id = str(hash(f"ddg_images:{p.platform}:{p.username}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES, {"job_id": job_id, "platform": p.platform, "username": p.username})

    async def metadata(self, p: DuckDuckGoMetadataRequest):
        job_id = str(hash(f"ddg_metadata:{p.platform}:{p.username}:{p.tokens}"))
        return await self.orion.social_trigger(job_id, SOCIAL_REQUEST_COMMANDS.S_DDG_METADATA, {"job_id": job_id, "platform": p.platform, "username": p.username, "tokens": p.tokens})
