import hashlib
from typing import Any

from starlette.requests import Request


class request_context_helper:
    @staticmethod
    def _header(request: Request, name: str) -> str:
        return str(request.headers.get(name, "") or "").strip()

    @classmethod
    def context_key(cls, request: Request) -> str:
        username = cls._header(request, "x-orion-user")
        user_id = cls._header(request, "x-orion-user-id")
        session_id = cls._header(request, "x-orion-session-id")
        return hashlib.sha256("|".join([username, user_id, session_id]).encode("utf-8")).hexdigest()

    @classmethod
    def with_request_context(cls, data: dict[str, Any], request: Request) -> dict[str, Any]:
        context = {
            "orion_user": cls._header(request, "x-orion-user"),
            "orion_user_id": cls._header(request, "x-orion-user-id"),
            "orion_tenant_id": cls._header(request, "x-orion-tenant-id"),
            "orion_session_id": cls._header(request, "x-orion-session-id"),
            "orion_session_client": cls._header(request, "x-orion-session-client") or "web",
        }
        return {**data, **{key: value for key, value in context.items() if value}}
