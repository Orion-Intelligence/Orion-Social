from __future__ import annotations

import asyncio
import base64
import json
import logging
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import Response

from api.orion.services.extension_manager.extension_job_manager import extension_job_manager
from api.orion.model.extension_models import (
    ConnectedExtension,
    ExtensionProgress,
    ExtensionLoginRequest,
    ExtensionRefreshRequest,
    ExtensionRegistration,
    ExtensionResult,
)
from api.orion.services.shared.helper_method import helper_method
from api.orion.services.extension_manager.extension_result_validator import (
    ExtensionResultValidationError,
    extension_result_validator,
)
from api.orion.services.shared.env_handler import env_handler


class extension_connection_manager:
    __instance = None
    _audit_logger = logging.getLogger("orion.extension.audit")

    @staticmethod
    def get_instance():
        if extension_connection_manager.__instance is None:
            extension_connection_manager()
        return extension_connection_manager.__instance

    def __init__(self):
        if extension_connection_manager.__instance is not None:
            return
        self.router = APIRouter()
        self.router.add_api_websocket_route("/extensions/ws", self.websocket_endpoint)
        self.router.add_api_route("/extensions/status", self.status, methods=["GET"])
        self.router.add_api_route("/extensions/download/chrome", self.download_chrome_extension, methods=["GET"])
        self.router.add_api_route("/extensions/download/firefox", self.download_firefox_extension, methods=["GET"])
        self.router.add_api_route("/extensions/auth/login", self.extension_auth_login, methods=["POST"])
        self.router.add_api_route("/extensions/auth/refresh", self.extension_auth_refresh, methods=["POST"])
        self._lock = asyncio.Lock()
        self._connections: dict[str, dict[str, Any]] = {}
        self._jobs = extension_job_manager.get_instance()
        self._max_message_bytes = int(self._env("ORION_EXTENSION_MAX_MESSAGE_BYTES", str(5 * 1024 * 1024)))
        extension_connection_manager.__instance = self

    async def websocket_endpoint(self, websocket: WebSocket):
        await websocket.accept()
        extension_id: str | None = None
        try:
            raw_registration = await asyncio.wait_for(websocket.receive_text(), timeout=10)
            registration = ExtensionRegistration(**self._decode(raw_registration))
            is_valid, reason, identity = await self._validate_registration(registration)
            if not is_valid:
                await websocket.close(code=1008, reason=reason)
                return

            extension = ConnectedExtension(
                capabilities=registration.capabilities,
                owner_username=str(identity.get("username") or ""),
                owner_session_id=str(identity.get("session_id") or ""),
                owner_session_client=str(identity.get("client") or ""),
            )
            extension_id = extension.extension_id
            await self._register(extension, websocket)
            self._audit("extension_registered", extension_id=extension_id, owner_username=extension.owner_username, session_client=extension.owner_session_client)
            await websocket.send_json({"type": "extension_registered", "extension_id": extension_id})

            while True:
                message = self._decode(await websocket.receive_text())
                await self._handle_message(extension_id, message)
        except WebSocketDisconnect:
            pass
        except asyncio.TimeoutError:
            await websocket.close(code=1008, reason="registration_timeout")
        except Exception as exc:
            try:
                await websocket.send_json({"type": "extension_error", "error": str(exc)})
            except Exception:
                pass
        finally:
            if extension_id:
                await self.unregister(extension_id)

    async def status(self) -> dict[str, Any]:
        async with self._lock:
            extensions = []
            for extension_id, state in self._connections.items():
                extension: ConnectedExtension = state["extension"]
                extensions.append({
                    "extension_id": extension_id,
                    "status": "online",
                    "platforms": sorted(extension.capabilities.normalized_platforms()),
                    "commands": sorted(extension.capabilities.normalized_commands()),
                    "owner_username": extension.owner_username,
                    "owner_session_client": extension.owner_session_client,
                    "connected_at": extension.connected_at,
                    "last_seen_at": extension.last_seen_at,
                    "active_job_id": extension.active_job_id,
                })
            return {"online": len(extensions), "extensions": extensions}

    async def download_extension(self, browser: str = "chrome") -> Response:
        is_firefox = browser.strip().lower() in {"firefox", "mozilla"}
        if is_firefox:
            artifact_path = self._extension_artifact_path("firefox", (".xpi",))
            if not artifact_path:
                raise HTTPException(
                    status_code=404,
                    detail="Signed Firefox XPI was not found in dist/extensions/firefox or ORION_FIREFOX_EXTENSION_XPI",
                )
            return Response(
                content=artifact_path.read_bytes(),
                media_type="application/x-xpinstall",
                headers={
                    "Content-Disposition": f'attachment; filename="{artifact_path.name}"',
                    "Cache-Control": "no-store",
                },
            )

        artifact_path = self._extension_artifact_path("chrome", (".zip",))
        if not artifact_path:
            raise HTTPException(
                status_code=404,
                detail="Chrome extension ZIP was not found in dist/extensions/chrome or ORION_CHROME_EXTENSION_ZIP",
            )

        return Response(
            content=artifact_path.read_bytes(),
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{artifact_path.name}"',
                "Cache-Control": "no-store",
            },
        )

    async def download_chrome_extension(self) -> Response:
        return await self.download_extension("chrome")

    async def download_firefox_extension(self) -> Response:
        return await self.download_extension("firefox")

    async def extension_auth_login(self, request: ExtensionLoginRequest) -> dict[str, Any]:
        username = str(request.username or "").strip()
        password = str(request.password or "")
        if not username or not password:
            raise HTTPException(status_code=400, detail="missing_credentials")
        return await asyncio.to_thread(
            self._post_orion_form_any_sync,
            self._orion_auth_login_urls(),
            {"username": username, "password": password, "scope": "orion_extension"},
        )

    async def extension_auth_refresh(self, request: ExtensionRefreshRequest) -> dict[str, Any]:
        token = str(request.token or "").strip()
        if not token:
            raise HTTPException(status_code=400, detail="missing_token")
        return await asyncio.to_thread(
            self._post_orion_json_any_sync,
            self._orion_auth_refresh_urls(),
            {"token": token},
            token,
        )

    async def _validate_registration(self, registration: ExtensionRegistration) -> tuple[bool, str, dict[str, str]]:
        allow_static_token = self._env("ORION_ALLOW_STATIC_EXTENSION_TOKEN", "0").strip().lower() in {"1", "true", "yes"}
        static_token = self._env("ORION_EXTENSION_TOKEN", "")
        if allow_static_token and static_token:
            return (registration.auth_token == static_token, "invalid_extension_token", {})

        require_auth = self._env("ORION_REQUIRE_EXTENSION_AUTH", "1").strip().lower() in {"1", "true", "yes"}
        if not registration.auth_token:
            return (False, "missing_extension_auth", {}) if require_auth else (True, "", {})

        refresh_urls = self._orion_auth_refresh_urls()
        if not refresh_urls:
            return True, "", {}

        identity = await asyncio.to_thread(self._validate_orion_token_sync, registration.auth_token, refresh_urls)
        is_valid = bool(identity)
        return (is_valid, "" if is_valid else "invalid_orion_session", identity or {})

    def _validate_orion_token_sync(self, token: str, refresh_urls: list[str]) -> dict[str, str] | None:
        payload = json.dumps({"token": token}).encode("utf-8")
        verify_tls = self._env("ORION_EXTENSION_AUTH_VERIFY_TLS", "0").strip().lower() in {"1", "true", "yes"}
        context = None if verify_tls else ssl._create_unverified_context()
        for refresh_url in refresh_urls:
            request = urllib.request.Request(
                refresh_url,
                data=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=8, context=context) as response:
                    if response.status >= 400:
                        continue
                    data = json.loads(response.read().decode("utf-8") or "{}")
                    access_token = str(data.get("access_token") or "").strip()
                    if access_token:
                        return self._identity_from_jwt_payload(access_token)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, json.JSONDecodeError):
                continue
        return None

    def _post_orion_form_any_sync(self, urls: list[str], form: dict[str, str]) -> dict[str, Any]:
        last_error: HTTPException | None = None
        for url in urls:
            try:
                return self._post_orion_form_sync(url, form)
            except HTTPException as exc:
                if not self._should_try_next_auth_url(exc.status_code):
                    raise
                last_error = exc
        raise last_error or HTTPException(status_code=502, detail="orion_auth_unreachable")

    def _post_orion_json_any_sync(self, urls: list[str], payload: dict[str, Any], bearer_token: str = "") -> dict[str, Any]:
        last_error: HTTPException | None = None
        for url in urls:
            try:
                return self._post_orion_json_sync(url, payload, bearer_token)
            except HTTPException as exc:
                if not self._should_try_next_auth_url(exc.status_code):
                    raise
                last_error = exc
        raise last_error or HTTPException(status_code=502, detail="orion_auth_unreachable")

    def _post_orion_form_sync(self, url: str, form: dict[str, str]) -> dict[str, Any]:
        payload = urllib.parse.urlencode(form).encode("utf-8")
        return self._open_orion_request_sync(
            urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
        )

    def _post_orion_json_sync(self, url: str, payload: dict[str, Any], bearer_token: str = "") -> dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"
        return self._open_orion_request_sync(
            urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
        )

    def _open_orion_request_sync(self, request: urllib.request.Request) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(request, timeout=15, context=self._orion_ssl_context()) as response:
                return json.loads(response.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as exc:
            detail = self._orion_error_detail(exc)
            raise HTTPException(status_code=exc.code, detail=detail)
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            raise HTTPException(status_code=502, detail=f"orion_auth_unreachable: {exc}")

    @classmethod
    def _identity_from_jwt_payload(cls, token: str) -> dict[str, str]:
        try:
            parts = token.split(".")
            if len(parts) < 2:
                return {}
            raw_payload = parts[1]
            raw_payload += "=" * (-len(raw_payload) % 4)
            payload = json.loads(base64.urlsafe_b64decode(raw_payload.encode("utf-8")).decode("utf-8") or "{}")
            username = str(payload.get("sub") or "").strip()
            session_id = str(payload.get("sid") or "").strip()
            client = str(payload.get("client") or "web").strip()
            if not username:
                return {}
            return {"username": username, "session_id": session_id, "client": client}
        except Exception:
            return {}

    @classmethod
    def _audit(cls, event: str, **fields: Any) -> None:
        payload = {
            "event": event,
            "component": "orion_social_extension",
            "at": cls._now(),
            **fields,
        }
        try:
            cls._audit_logger.info(json.dumps(payload, default=str, sort_keys=True))
        except Exception:
            cls._audit_logger.info("orion_social_extension_audit_failed")

    @staticmethod
    def _json_size(value: Any) -> int:
        try:
            return len(json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8"))
        except Exception:
            return 0

    @staticmethod
    def _safe_error_text(value: Any) -> str:
        return str(value or "extension_job_failed").replace("\x00", "")[:500]

    @staticmethod
    def _safe_error_code(value: Any) -> str | None:
        code = "".join(char for char in str(value or "").upper() if char.isalnum() or char == "_")[:80]
        return code or None

    @staticmethod
    def _safe_error_url(value: Any, platform: str | None = None) -> str | None:
        url = str(value or "").strip()
        if not url:
            return None
        try:
            parsed = urllib.parse.urlparse(url)
        except Exception:
            return None
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return None
        allowed_hosts = {
            "instagram": ("instagram.com",),
            "facebook": ("facebook.com",),
            "x": ("x.com", "twitter.com"),
            "twitter": ("x.com", "twitter.com"),
            "linkedin": ("linkedin.com",),
            "reddit": ("reddit.com",),
            "github": ("github.com",),
            "youtube": ("youtube.com", "youtu.be"),
            "tiktok": ("tiktok.com",),
        }.get(helper_method.normalize_platform(platform or ""), ())
        if not allowed_hosts:
            return None
        hostname = (parsed.hostname or "").lower()
        if not any(hostname == host or hostname.endswith(f".{host}") for host in allowed_hosts):
            return None
        return url[:1000]

    @staticmethod
    def _env(key: str, default: str | None = None) -> str:
        return str(env_handler.get_instance().env(key, default) or "")

    def _orion_auth_login_urls(self) -> list[str]:
        return [f"{base_url}/token" for base_url in self._orion_auth_base_urls()]

    def _orion_auth_refresh_urls(self) -> list[str]:
        refresh_url = self._env("ORION_EXTENSION_AUTH_REFRESH_URL", "").strip()
        candidates = [refresh_url] if refresh_url else []
        candidates.extend(f"{base_url}/token/refresh" for base_url in self._orion_auth_base_urls())
        return self._unique_urls(candidates)

    def _orion_auth_base_url(self) -> str:
        return self._orion_auth_base_urls()[0]

    def _orion_auth_base_urls(self) -> list[str]:
        base_url = self._env("ORION_EXTENSION_AUTH_BASE_URL", "").strip()
        candidates = [base_url] if base_url else []

        refresh_url = self._env("ORION_EXTENSION_AUTH_REFRESH_URL", "").strip()
        marker = "/token/refresh"
        if refresh_url.endswith(marker):
            candidates.append(refresh_url[: -len(marker)].rstrip("/"))

        candidates.extend([
            "http://trusted-web-main:8070/api",
            "https://host.docker.internal:8443/api",
            "http://host.docker.internal:8080/api",
            "https://127.0.0.1:8443/api",
            "http://127.0.0.1:8080/api",
            "https://localhost:8443/api",
            "http://localhost:8080/api",
        ])
        return self._unique_urls(candidates)

    @staticmethod
    def _unique_urls(urls: list[str]) -> list[str]:
        unique_urls: list[str] = []
        seen: set[str] = set()
        for url in urls:
            normalized_url = str(url or "").strip().rstrip("/")
            if not normalized_url or normalized_url in seen:
                continue
            seen.add(normalized_url)
            unique_urls.append(normalized_url)
        return unique_urls

    def _orion_ssl_context(self):
        verify_tls = self._env("ORION_EXTENSION_AUTH_VERIFY_TLS", "0").strip().lower() in {"1", "true", "yes"}
        return None if verify_tls else ssl._create_unverified_context()

    @staticmethod
    def _should_try_next_auth_url(status_code: int) -> bool:
        return int(status_code) in {404, 405, 502}

    @staticmethod
    def _orion_error_detail(exc: urllib.error.HTTPError) -> Any:
        try:
            raw = exc.read().decode("utf-8")
            data = json.loads(raw or "{}")
            return data.get("detail", data)
        except Exception:
            return exc.reason or str(exc)

    @classmethod
    def _extension_artifact_path(cls, browser: str, suffixes: tuple[str, ...]) -> Path | None:
        env_path = cls._env(cls._extension_artifact_env_key(browser), "").strip()
        if env_path:
            candidate = Path(env_path).expanduser()
            if not candidate.is_absolute():
                candidate = Path.cwd() / candidate
            if candidate.is_file() and candidate.suffix.lower() in suffixes:
                return candidate

        current_file = Path(__file__).resolve()
        roots = [
            current_file.parents[3],  # /app in Docker
            current_file.parents[4],  # repo root in local development
            Path.cwd(),
            Path.cwd().parent,
        ]
        candidates: list[Path] = []
        for root in roots:
            artifact_dir = root / "dist/extensions" / browser
            if artifact_dir.is_dir():
                candidates.extend(
                    path for path in artifact_dir.iterdir()
                    if path.is_file() and path.suffix.lower() in suffixes
                )
        if not candidates:
            return None
        return max(candidates, key=lambda path: path.stat().st_mtime)

    @staticmethod
    def _extension_artifact_env_key(browser: str) -> str:
        return "ORION_FIREFOX_EXTENSION_XPI" if browser == "firefox" else "ORION_CHROME_EXTENSION_ZIP"

    async def find_available(self, platform: str, command: str, owner_username: str = "", owner_session_id: str = "") -> str | None:
        platform = helper_method.normalize_platform(platform)
        command = str(command or "").strip().lower()
        owner_username = str(owner_username or "").strip().lower()
        owner_session_id = str(owner_session_id or "").strip()
        require_same_session = self._env("ORION_EXTENSION_REQUIRE_SAME_SESSION", "0").strip().lower() in {"1", "true", "yes"}
        async with self._lock:
            for extension_id, state in self._connections.items():
                extension: ConnectedExtension = state["extension"]
                if extension.active_job_id:
                    continue
                if owner_username and extension.owner_username.lower() != owner_username:
                    continue
                if require_same_session and owner_session_id and extension.owner_session_id != owner_session_id:
                    continue
                platforms = extension.capabilities.normalized_platforms()
                commands = extension.capabilities.normalized_commands()
                if platform in platforms and (not commands or command in commands):
                    return extension_id
        return None

    async def send_job(self, extension_id: str, payload: dict[str, Any]) -> bool:
        async with self._lock:
            state = self._connections.get(extension_id)
            if not state:
                return False
            websocket: WebSocket = state["websocket"]
            extension: ConnectedExtension = state["extension"]
            extension.active_job_id = str(payload.get("job", {}).get("job_id") or payload.get("job_id") or "")
            extension.last_seen_at = self._now()
        try:
            await websocket.send_json(payload)
            job = payload.get("job", {}) if isinstance(payload.get("job"), dict) else {}
            self._audit(
                "extension_job_sent",
                extension_id=extension_id,
                job_id=str(job.get("job_id") or ""),
                platform=str(job.get("platform") or ""),
                command=str(job.get("command") or ""),
                owner_username=str(job.get("owner_username") or ""),
            )
            return True
        except Exception:
            await self.unregister(extension_id)
            return False

    async def release_job(self, extension_id: str, job_id: str) -> None:
        async with self._lock:
            state = self._connections.get(extension_id)
            if not state:
                return
            extension: ConnectedExtension = state["extension"]
            if extension.active_job_id == job_id:
                extension.active_job_id = None
                extension.last_seen_at = self._now()

    async def unregister(self, extension_id: str) -> None:
        async with self._lock:
            state = self._connections.pop(extension_id, None)
        if state:
            extension: ConnectedExtension = state["extension"]
            active_job_id = extension.active_job_id
            self._audit("extension_unregistered", extension_id=extension_id, owner_username=extension.owner_username, active_job_id=active_job_id)
            if active_job_id:
                job_state = await self._jobs.get(active_job_id)
                if job_state and job_state.get("status") not in {"done", "error"}:
                    await self._jobs.fail(active_job_id, "extension_disconnected")

    async def _register(self, extension: ConnectedExtension, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections[extension.extension_id] = {
                "extension": extension,
                "websocket": websocket,
            }

    async def _handle_message(self, extension_id: str, message: dict[str, Any]) -> None:
        message_type = message.get("type")
        active_job_id = None
        websocket: WebSocket | None = None
        async with self._lock:
            state = self._connections.get(extension_id)
            if state:
                websocket = state["websocket"]
                extension: ConnectedExtension = state["extension"]
                extension.last_seen_at = self._now()
                active_job_id = extension.active_job_id

        if message_type == "heartbeat":
            return

        if message_type == "extension_error":
            job_id = str(message.get("job_id") or active_job_id or "")
            if job_id:
                if not await self._jobs.is_assigned_to(job_id, extension_id):
                    raise ValueError("extension_error_job_not_assigned")
                error = str(message.get("error") or "extension_error")[:500]
                self._audit("extension_job_error", extension_id=extension_id, job_id=job_id, error=error)
                await self._jobs.fail(job_id, error)
                await self.release_job(extension_id, job_id)
            return

        if message_type == "job_progress":
            progress = ExtensionProgress(**message)
            if not await self._jobs.is_assigned_to(progress.job_id, extension_id):
                raise ValueError("extension_progress_job_not_assigned")
            await self._jobs.progress(progress)
            return

        if message_type == "job_result":
            result = ExtensionResult(**message)
            ack_id = str(message.get("ack_id") or "")
            job = await self._jobs.assigned_job(result.job_id, extension_id)
            if not job:
                await self._send_result_ack(websocket, result.job_id, ack_id, accepted=False, error="extension_result_job_not_assigned")
                return
            if result.success:
                try:
                    result.data = extension_result_validator.validate_result_data(job, result.data)
                except ExtensionResultValidationError as exc:
                    self._audit(
                        "extension_result_rejected",
                        extension_id=extension_id,
                        job_id=result.job_id,
                        platform=job.platform,
                        command=job.command,
                        owner_username=job.owner_username,
                        error=str(exc),
                    )
                    await self._jobs.fail(result.job_id, str(exc))
                    await self.release_job(extension_id, result.job_id)
                    await self._send_result_ack(websocket, result.job_id, ack_id, accepted=False, error=str(exc))
                    return
                self._audit(
                    "extension_result_accepted",
                    extension_id=extension_id,
                    job_id=result.job_id,
                    platform=job.platform,
                    command=job.command,
                    owner_username=job.owner_username,
                    result_size_bytes=self._json_size(result.data),
                    untrusted=True,
                )
            else:
                result.data = None
                result.error = self._safe_error_text(result.error or result.message or "extension_job_failed")
                result.message = self._safe_error_text(result.message or result.error)
                result.error_code = self._safe_error_code(result.error_code)
                result.platform = helper_method.normalize_platform(result.platform or job.platform)
                result.login_url = self._safe_error_url(result.login_url, result.platform)
                self._audit(
                    "extension_result_error",
                    extension_id=extension_id,
                    job_id=result.job_id,
                    platform=job.platform,
                    command=job.command,
                    owner_username=job.owner_username,
                    error=result.error,
                    error_code=result.error_code,
                    login_url_present=bool(result.login_url),
                    untrusted=True,
                )
            await self._jobs.complete(result)
            await self.release_job(extension_id, result.job_id)
            await self._send_result_ack(websocket, result.job_id, ack_id, accepted=True)

    async def _send_result_ack(self, websocket: WebSocket | None, job_id: str, ack_id: str = "", accepted: bool = True, error: str = "") -> None:
        if not websocket:
            return
        payload: dict[str, Any] = {
            "type": "job_result_ack",
            "job_id": job_id,
            "accepted": accepted,
        }
        if ack_id:
            payload["ack_id"] = ack_id
        if error:
            payload["error"] = self._safe_error_text(error)
        try:
            await websocket.send_json(payload)
        except Exception:
            pass

    def _decode(self, raw_data: str) -> dict[str, Any]:
        if len(raw_data.encode("utf-8")) > self._max_message_bytes:
            raise ValueError("extension_message_too_large")
        data = json.loads(raw_data)
        if not isinstance(data, dict):
            raise ValueError("message_must_be_object")
        return data

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
