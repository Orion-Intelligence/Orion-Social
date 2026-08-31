from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProfileCheck:
    platform: str
    username: str
    verdict: str
    url: str = ""
    info: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    status_code: int | None = None
    final_url: str = ""
    target_type: str = "profile"
