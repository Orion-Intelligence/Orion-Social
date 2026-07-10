from __future__ import annotations

import asyncio
import os
from typing import Any
from uuid import uuid4

from api.orion.extension_manager.extension_connection_manager import extension_connection_manager
from api.orion.extension_manager.extension_job_manager import extension_job_manager
from api.orion.extension_manager.extension_models import ExtensionJob, normalize_platform
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class extension_executor:
    __instance = None

    SUPPORTED_COMMANDS = {
        SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY: "profile",
        SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY: "followers",
        SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY: "following",
        SOCIAL_REQUEST_COMMANDS.S_POSTS: "posts",
        SOCIAL_REQUEST_COMMANDS.S_VIDEOS: "videos",
        SOCIAL_REQUEST_COMMANDS.S_SHORTS: "shorts",
        SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES: "images",
    }

    DEFAULT_PLATFORMS = {"reddit", "github", "linkedin", "x", "instagram", "facebook"}

    @staticmethod
    def get_instance():
        if extension_executor.__instance is None:
            extension_executor()
        return extension_executor.__instance

    def __init__(self):
        if extension_executor.__instance is not None:
            return
        self._connections = extension_connection_manager.get_instance()
        self._jobs = extension_job_manager.get_instance()
        extension_executor.__instance = self

    def supports(self, command: int, data: dict[str, Any]) -> bool:
        if os.getenv("ORION_EXTENSION_EXECUTOR_ENABLED", "1").strip().lower() in {"0", "false", "no"}:
            return False
        if command not in self.SUPPORTED_COMMANDS:
            return False
        platform = normalize_platform(str(data.get("platform") or ""))
        if not platform:
            return False
        return platform in self._configured_platforms()

    async def dispatch_and_wait(self, command: int, data: dict[str, Any], timeout: int = 600) -> dict[str, Any] | None:
        if not self.supports(command, data):
            return None

        job = self._build_job(command, data)
        extension_id = await self._connections.find_available(job.platform, job.command, job.owner_username, job.owner_session_id)
        if not extension_id:
            await self._jobs.mark_waiting(job.job_id)
            if data.get("use_extension"):
                return await self._wait_for_extension(job, timeout)
            return None if self._fallback_enabled() else await self._wait_for_extension(job, timeout)

        future = await self._jobs.create_job(job)
        await self._jobs.mark_assigned(job.job_id, extension_id)
        sent = await self._connections.send_job(extension_id, {"type": "job", "job": self._model_dump(job)})
        if not sent:
            await self._jobs.fail(job.job_id, "extension_dispatch_failed")
            if data.get("use_extension"):
                return await future
            return None if self._fallback_enabled() else await future

        try:
            result = await asyncio.wait_for(future, timeout=timeout)
            return result
        except asyncio.TimeoutError:
            await self._jobs.fail(job.job_id, "extension_timeout")
            if data.get("use_extension"):
                return {"status": "error", "executor": "extension", "error": "extension_timeout", "data": None}
            return None if self._fallback_enabled() else {"status": "error", "executor": "extension", "error": "extension_timeout", "data": None}
        finally:
            await self._connections.release_job(extension_id, job.job_id)
            await self._jobs.remove(job.job_id)

    async def _wait_for_extension(self, job: ExtensionJob, timeout: int) -> dict[str, Any]:
        future = await self._jobs.create_job(job)
        await self._jobs.mark_waiting(job.job_id)
        deadline = asyncio.get_running_loop().time() + timeout
        extension_id = None
        try:
            while asyncio.get_running_loop().time() < deadline:
                extension_id = await self._connections.find_available(job.platform, job.command, job.owner_username, job.owner_session_id)
                if extension_id:
                    await self._jobs.mark_assigned(job.job_id, extension_id)
                    sent = await self._connections.send_job(extension_id, {"type": "job", "job": self._model_dump(job)})
                    if sent:
                        break
                    extension_id = None
                await asyncio.sleep(2)
            else:
                raise asyncio.TimeoutError

            remaining = max(1, int(deadline - asyncio.get_running_loop().time()))
            return await asyncio.wait_for(future, timeout=remaining)
        except asyncio.TimeoutError:
            await self._jobs.fail(job.job_id, "extension_unavailable")
            return {"status": "error", "executor": "extension", "error": "extension_unavailable", "data": None}
        finally:
            if extension_id:
                await self._connections.release_job(extension_id, job.job_id)
            await self._jobs.remove(job.job_id)

    def _build_job(self, command: int, data: dict[str, Any]) -> ExtensionJob:
        platform = normalize_platform(str(data.get("platform") or ""))
        username = str(data.get("username") or "").strip().lstrip("@")
        command_name = self.SUPPORTED_COMMANDS[command]
        return ExtensionJob(
            job_id=str(data.get("job_id") or uuid4()),
            command=command_name,
            platform=platform,
            username=username,
            url=str(data.get("url") or self._profile_url(platform, username)),
            owner_username=str(data.get("orion_user") or ""),
            owner_user_id=str(data.get("orion_user_id") or ""),
            owner_tenant_id=str(data.get("orion_tenant_id") or ""),
            owner_session_id=str(data.get("orion_session_id") or ""),
            owner_session_client=str(data.get("orion_session_client") or "web"),
            social_data_type=str(data.get("social_data_type") or command_name),
            limits={
                "max_posts": self._int_value(data.get("max_posts"), 20),
                "post_offset": self._int_value(data.get("post_offset"), 0),
                "existing_posts_count": self._int_value(data.get("existing_posts_count"), 0),
                "max_comments": self._int_value(data.get("max_comments"), 25),
                "max_images": self._int_value(data.get("max_images"), 25),
                "max_followers": self._int_value(data.get("max_followers"), 1000),
                "max_following": self._int_value(data.get("max_following"), 1000),
                "max_videos": self._int_value(data.get("max_videos"), 25),
                "max_shorts": self._int_value(data.get("max_shorts"), 25),
            },
            cursor={
                "hash_id": str(data.get("hash_id") or ""),
                "existing_post_urls": self._list_value(data.get("existing_post_urls")),
            },
        )

    def _configured_platforms(self) -> set[str]:
        raw_value = os.getenv("ORION_EXTENSION_PLATFORMS", "")
        if not raw_value.strip():
            return set(self.DEFAULT_PLATFORMS)
        return {normalize_platform(item) for item in raw_value.split(",") if item.strip()}

    @staticmethod
    def _fallback_enabled() -> bool:
        return os.getenv("ORION_EXTENSION_FALLBACK_ENABLED", "1").strip().lower() not in {"0", "false", "no"}

    @staticmethod
    def _profile_url(platform: str, username: str) -> str:
        urls = {
            "reddit": f"https://www.reddit.com/user/{username}/",
            "linkedin": f"https://www.linkedin.com/in/{username}/",
            "x": f"https://x.com/{username}",
            "instagram": f"https://www.instagram.com/{username}/",
            "facebook": f"https://www.facebook.com/{username}",
            "github": f"https://github.com/{username}",
        }
        return urls.get(platform, username)

    @staticmethod
    def _int_value(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _list_value(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value if item]
        return []

    @staticmethod
    def _model_dump(model: ExtensionJob) -> dict[str, Any]:
        if hasattr(model, "model_dump"):
            return model.model_dump()
        return model.dict()
