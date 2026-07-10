from __future__ import annotations

import json
import math
import os
import re
from typing import Any
from urllib.parse import urlparse

from api.orion.extension_manager.extension_models import ExtensionJob, normalize_platform


class ExtensionResultValidationError(ValueError):
    pass


class extension_result_validator:
    MAX_RESULT_BYTES = int(os.getenv("ORION_EXTENSION_MAX_RESULT_BYTES", str(2 * 1024 * 1024)))
    MAX_STRING_LENGTH = int(os.getenv("ORION_EXTENSION_MAX_STRING_LENGTH", "5000"))
    MAX_URL_LENGTH = int(os.getenv("ORION_EXTENSION_MAX_URL_LENGTH", "2048"))
    MAX_NESTING_DEPTH = int(os.getenv("ORION_EXTENSION_MAX_NESTING_DEPTH", "8"))
    MAX_OBJECT_KEYS = int(os.getenv("ORION_EXTENSION_MAX_OBJECT_KEYS", "80"))
    MAX_ERRORS = 20
    MAX_COMMENTS = 100
    MAX_POSTS = 100
    MAX_IMAGES = 100
    MAX_CONNECTIONS = 5000

    BLOCKED_KEYS = {"__proto__", "constructor", "prototype"}
    URL_KEYS = {"url", "profile_url", "post_url", "source_url", "media_url", "image_url", "thumbnail", "avatar_url", "cover_url", "website"}
    TOP_LEVEL_KEYS = {
        "platform",
        "username",
        "requested_username",
        "url",
        "profile",
        "profile_details",
        "profileDetails",
        "posts",
        "videos",
        "shorts",
        "images",
        "followers",
        "following",
        "partial",
        "errors",
    }
    PROFILE_KEYS = {
        "username",
        "display_name",
        "full_name",
        "real_name",
        "bio",
        "description",
        "url",
        "profile_url",
        "avatar_url",
        "cover_url",
        "posts_count",
        "followers_count",
        "following_count",
        "total_posts",
        "total_followers",
        "total_following",
        "website",
        "location",
        "company",
        "status",
    }
    POST_KEYS = {
        "id",
        "hash_id",
        "title",
        "text",
        "caption",
        "url",
        "post_url",
        "datetime",
        "created_at",
        "timestamp",
        "author",
        "source",
        "score",
        "likes",
        "likes_count",
        "comments",
        "comments_count",
        "views",
        "views_count",
        "shares",
        "retweets",
        "media_type",
        "media_url",
        "image_url",
        "thumbnail",
        "comment_items",
        "comment_details",
    }
    IMAGE_KEYS = {"image_url", "thumbnail", "source_url", "title", "source"}
    COMMENT_KEYS = {"sender_name", "username", "text", "date", "likes"}
    ERROR_KEYS = {"step", "message"}

    @classmethod
    def validate_result_data(cls, job: ExtensionJob, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise ExtensionResultValidationError("extension_result_data_must_be_object")

        cls._ensure_json_size(data)
        platform = normalize_platform(str(data.get("platform") or job.platform))
        if platform and platform != normalize_platform(job.platform):
            raise ExtensionResultValidationError("extension_result_platform_mismatch")

        sanitized: dict[str, Any] = {
            "platform": normalize_platform(job.platform),
            "requested_username": cls._sanitize_username(job.username),
            "_orion_trust": {
                "trusted": False,
                "untrusted": True,
                "source": "browser_extension",
                "validation_status": "sanitized",
            },
        }

        for key, value in data.items():
            if key in cls.BLOCKED_KEYS or key not in cls.TOP_LEVEL_KEYS:
                continue
            if key in {"platform", "requested_username"}:
                continue
            if key == "username":
                sanitized[key] = cls._sanitize_username(value)
            elif key == "url":
                sanitized[key] = cls._sanitize_url(value)
            elif key in {"profile", "profile_details", "profileDetails"}:
                profile = cls._sanitize_record(value, cls.PROFILE_KEYS)
                if profile:
                    sanitized["profile"] = profile
            elif key in {"posts", "videos", "shorts"}:
                sanitized[key] = cls._sanitize_posts(value, job, key)
            elif key == "images":
                sanitized[key] = cls._sanitize_images(value, job)
            elif key in {"followers", "following"}:
                sanitized[key] = cls._sanitize_connection_list(value, job, key)
            elif key == "partial":
                sanitized[key] = bool(value)
            elif key == "errors":
                sanitized[key] = cls._sanitize_errors(value)

        cls._ensure_json_size(sanitized)
        return sanitized

    @classmethod
    def _sanitize_record(cls, value: Any, allowed_keys: set[str]) -> dict[str, Any]:
        if not isinstance(value, dict):
            return {}
        result: dict[str, Any] = {}
        for key, item in list(value.items())[: cls.MAX_OBJECT_KEYS]:
            clean_key = cls._sanitize_key(key)
            if not clean_key or clean_key in cls.BLOCKED_KEYS or clean_key not in allowed_keys:
                continue
            if clean_key in cls.URL_KEYS:
                clean_value = cls._sanitize_url(item)
            else:
                clean_value = cls._sanitize_scalar(item)
            if clean_value not in {"", None}:
                result[clean_key] = clean_value
        return result

    @classmethod
    def _sanitize_posts(cls, value: Any, job: ExtensionJob, key: str) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        limit_key = {"posts": "max_posts", "videos": "max_videos", "shorts": "max_shorts"}[key]
        limit = cls._bounded_limit(job.limits.get(limit_key), cls.MAX_POSTS)
        posts: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in value[:limit]:
            raw_comment_items = item.get("comment_items") if isinstance(item, dict) else None
            raw_comment_details = item.get("comment_details") if isinstance(item, dict) else None
            post = cls._sanitize_record(item, cls.POST_KEYS)
            if not post:
                continue
            post["comment_items"] = cls._sanitize_comment_items(raw_comment_items, job)
            post["comment_details"] = cls._sanitize_comment_details(raw_comment_details, job)
            identity = str(post.get("post_url") or post.get("url") or post.get("id") or post.get("hash_id") or json.dumps(post, sort_keys=True))
            if identity in seen:
                continue
            seen.add(identity)
            posts.append(post)
        return posts

    @classmethod
    def _sanitize_images(cls, value: Any, job: ExtensionJob) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        limit = cls._bounded_limit(job.limits.get("max_images"), cls.MAX_IMAGES)
        images: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in value[:limit]:
            image = cls._sanitize_record(item, cls.IMAGE_KEYS)
            image_url = str(image.get("image_url") or image.get("thumbnail") or "")
            if not image_url or image_url in seen:
                continue
            seen.add(image_url)
            images.append(image)
        return images

    @classmethod
    def _sanitize_connection_list(cls, value: Any, job: ExtensionJob, key: str) -> list[str]:
        if not isinstance(value, list):
            return []
        limit_key = "max_followers" if key == "followers" else "max_following"
        limit = cls._bounded_limit(job.limits.get(limit_key), cls.MAX_CONNECTIONS)
        users: list[str] = []
        seen: set[str] = set()
        for item in value[:limit]:
            username = cls._sanitize_username(item)
            normalized = username.lower()
            if not username or normalized in seen:
                continue
            seen.add(normalized)
            users.append(username)
        return users

    @classmethod
    def _sanitize_comment_items(cls, value: Any, job: ExtensionJob) -> list[str]:
        if not isinstance(value, list):
            return []
        limit = cls._bounded_limit(job.limits.get("max_comments"), cls.MAX_COMMENTS)
        return [item for item in (cls._sanitize_text(item, 2000) for item in value[:limit]) if item]

    @classmethod
    def _sanitize_comment_details(cls, value: Any, job: ExtensionJob) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        limit = cls._bounded_limit(job.limits.get("max_comments"), cls.MAX_COMMENTS)
        comments: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in value[:limit]:
            comment = cls._sanitize_record(item, cls.COMMENT_KEYS)
            if not comment:
                continue
            identity = "|".join(str(comment.get(part) or "") for part in ("sender_name", "date", "text"))
            if identity in seen:
                continue
            seen.add(identity)
            comments.append(comment)
        return comments

    @classmethod
    def _sanitize_errors(cls, value: Any) -> list[dict[str, str]]:
        if not isinstance(value, list):
            return []
        errors: list[dict[str, str]] = []
        for item in value[: cls.MAX_ERRORS]:
            if isinstance(item, dict):
                step = cls._sanitize_text(item.get("step"), 120)
                message = cls._sanitize_text(item.get("message"), 500)
            else:
                step = ""
                message = cls._sanitize_text(item, 500)
            if message:
                errors.append({"step": step, "message": message})
        return errors

    @classmethod
    def _sanitize_scalar(cls, value: Any) -> str | int | float | bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return value if math.isfinite(value) else ""
        return cls._sanitize_text(value, cls.MAX_STRING_LENGTH)

    @classmethod
    def _sanitize_username(cls, value: Any) -> str:
        username = cls._sanitize_text(value, 120).lstrip("@")
        username = re.sub(r"[^A-Za-z0-9_.-]", "", username)
        return username[:80]

    @classmethod
    def _sanitize_url(cls, value: Any) -> str:
        url = cls._sanitize_text(value, cls.MAX_URL_LENGTH)
        if not url:
            return ""
        parsed = urlparse(url)
        if parsed.scheme.lower() not in {"http", "https"}:
            return ""
        if not parsed.netloc or parsed.username or parsed.password:
            return ""
        return url

    @classmethod
    def _sanitize_key(cls, value: Any) -> str:
        key = str(value or "").strip()
        if key in cls.BLOCKED_KEYS:
            return ""
        return re.sub(r"[^A-Za-z0-9_]", "", key)[:80]

    @classmethod
    def _sanitize_text(cls, value: Any, max_length: int) -> str:
        text = "" if value is None else str(value)
        text = text.replace("\x00", "")
        text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
        text = re.sub(r"(?is)<script\b[^>]*>.*?</script>", "", text)
        text = re.sub(r"(?is)<style\b[^>]*>.*?</style>", "", text)
        text = re.sub(r"(?s)<[^>]{1,200}>", "", text)
        return text.strip()[:max_length]

    @classmethod
    def _bounded_limit(cls, value: Any, cap: int) -> int:
        try:
            limit = int(value)
        except (TypeError, ValueError):
            limit = cap
        return max(0, min(limit, cap))

    @classmethod
    def _ensure_json_size(cls, value: Any) -> None:
        try:
            raw = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError) as exc:
            raise ExtensionResultValidationError("extension_result_not_json_serializable") from exc
        if len(raw.encode("utf-8")) > cls.MAX_RESULT_BYTES:
            raise ExtensionResultValidationError("extension_result_too_large")
