from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field
from api.orion.services.shared.helper_method import helper_method


class ExtensionCapabilities(BaseModel):
    platforms: list[str] = Field(default_factory=list)
    commands: list[str] = Field(default_factory=list)

    def normalized_platforms(self) -> set[str]:
        return {helper_method.normalize_platform(platform) for platform in self.platforms if platform}

    def normalized_commands(self) -> set[str]:
        return {str(command or "").strip().lower() for command in self.commands if command}


class ExtensionRegistration(BaseModel):
    type: str = "extension_online"
    auth_token: str = ""
    auth_type: str = ""
    capabilities: ExtensionCapabilities = Field(default_factory=ExtensionCapabilities)


class ExtensionLoginRequest(BaseModel):
    username: str = ""
    password: str = ""


class ExtensionRefreshRequest(BaseModel):
    token: str = ""


class ExtensionJob(BaseModel):
    job_id: str
    command: str
    platform: str
    username: str
    url: str
    owner_username: str = ""
    owner_user_id: str = ""
    owner_tenant_id: str = ""
    owner_session_id: str = ""
    owner_session_client: str = "web"
    social_data_type: str = "profile_info"
    limits: dict[str, int] = Field(default_factory=dict)
    cursor: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ExtensionProgress(BaseModel):
    type: str = "job_progress"
    job_id: str
    status: str = "pending"
    step: str = "extension_assigned"
    progress: int = 15


class ExtensionResult(BaseModel):
    type: str = "job_result"
    job_id: str
    status: str = "done"
    success: bool = True
    data: Any = None
    error: str | None = None
    message: str | None = None
    error_code: str | None = None
    platform: str | None = None
    login_url: str | None = None


class ConnectedExtension(BaseModel):
    extension_id: str = Field(default_factory=lambda: str(uuid4()))
    owner_username: str = ""
    owner_session_id: str = ""
    owner_session_client: str = ""
    capabilities: ExtensionCapabilities = Field(default_factory=ExtensionCapabilities)
    connected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    active_job_id: str | None = None



