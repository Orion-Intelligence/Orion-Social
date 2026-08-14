from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PlatformProbeSpec:
    platform: str
    module_name: str
    file_path: str


@dataclass
class ProbeResult:
    probe: str
    target: str
    status: str
    elapsed_ms: int
    reason: str = ""
    details: dict[str, Any] = field(default_factory=dict)

