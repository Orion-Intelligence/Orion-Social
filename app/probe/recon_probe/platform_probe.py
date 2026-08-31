from __future__ import annotations

import argparse
import concurrent.futures
import importlib
import inspect
import re
import time
import traceback
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlparse

from app.probe.recon_probe.constant.recon_probe_constant import ReconProbeConstants
from app.probe.recon_probe.model.recon_probe_model import PlatformProbeSpec, ProbeResult
from app.probe.recon_probe.probe_base import _ProbeBase


class PlatformProbe(_ProbeBase):
    def invoke_probe(self, argv: list[str] | None = None) -> int:
        args = self._build_parser().parse_args(argv)
        if args.worker:
            return self._emit_worker_result(self._probe_worker(args.worker))

        workers = max(1, min(args.workers, 8))
        if args.timeout <= 0:
            raise SystemExit("--timeout must be greater than zero")
        selected = {value.strip().lower() for value in (args.platform or []) if value.strip()}
        specs = self._discover_platforms(selected)
        if not specs:
            print("No platform probe modules matched the selection.")
            return 2

        print(f"Discovered {len(specs)} platform probe modules; workers={workers}; timeout={args.timeout:g}s", flush=True)
        results: list[ProbeResult] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    self._run_worker,
                    ReconProbeConstants.PLATFORM_SCRIPT_MODULE,
                    ["--worker", spec.platform],
                    "platform",
                    spec.platform,
                    args.timeout,
                ): spec
                for spec in specs
            }
            for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
                spec = futures[future]
                try:
                    result = future.result()
                except Exception as exc:
                    result = ProbeResult("platform", spec.platform, "ERROR", 0, f"orchestrator {type(exc).__name__}: {exc}")
                results.append(result)
                self._print_result(index, len(specs), result)
        return self._finish_results(results, args.output)

    @staticmethod
    def _discover_platforms(selected: set[str] | None = None) -> list[PlatformProbeSpec]:
        selected = selected or set()
        specs: list[PlatformProbeSpec] = []
        for file_path in sorted(ReconProbeConstants.PLATFORM_ROOT.glob("*.py")):
            if file_path.stem.startswith("_"):
                continue
            platform = file_path.stem.lower()
            if selected and platform not in selected:
                continue
            specs.append(
                PlatformProbeSpec(
                    platform=platform,
                    module_name=f"{ReconProbeConstants.PLATFORM_MODULE_PREFIX}.{platform}",
                    file_path=str(file_path),
                )
            )
        return specs

    def _probe_worker(self, platform: str) -> ProbeResult:
        started = time.monotonic()
        result = ProbeResult("platform", platform, "ERROR", 0)
        try:
            self._configure_import_paths()
            module_name = f"{ReconProbeConstants.PLATFORM_MODULE_PREFIX}.{platform}"
            module = importlib.import_module(module_name)
            import api.social_manager.social_recon.custom_recon.core.registry as registry

            if registry.resolve(platform) is not module:
                raise ValueError(f"{platform} is not registered to {module_name}")

            constant_class = getattr(module, "constants", None)
            if not inspect.isclass(constant_class):
                raise TypeError("constants is missing or is not a class")
            missing = [member for member in ReconProbeConstants.REQUIRED_PLATFORM_MEMBERS if not hasattr(constant_class, member)]
            if missing:
                raise AttributeError("constant class is missing members: " + ", ".join(missing))

            name = constant_class.NAME
            profile_template = constant_class.PROFILE_URL
            if not isinstance(name, str) or not name.strip():
                raise TypeError("NAME must be a non-empty string")
            if not isinstance(profile_template, str) or "{username}" not in profile_template:
                raise ValueError("PROFILE_URL must contain {username}")

            profile_url = profile_template.format(username=ReconProbeConstants.SAMPLE_USERNAME)
            self._require_https_url(profile_url, "PROFILE_URL")
            supported = getattr(constant_class, "SUPPORTED", True)
            crawl_type = getattr(constant_class, "CRAWL_TYPE", "normal")
            details = {"module": module_name, "name": name, "supported": bool(supported), "crawl_type": crawl_type, "profile_url": profile_url}

            if crawl_type == "unverified":
                if not getattr(module, "ROUTES", ()) and not getattr(module, "SUBDOMAIN", None):
                    raise ValueError("unverified modules must define ROUTES or SUBDOMAIN")
            elif not supported:
                reason = getattr(constant_class, "REASON", "")
                if not isinstance(reason, str) or not reason.strip():
                    raise ValueError("unsupported modules must define REASON")
                details["unsupported_reason"] = reason
            else:
                grammar = getattr(constant_class, "GRAMMAR", None)
                if not isinstance(grammar, str) or not grammar:
                    raise ValueError("GRAMMAR must be a non-empty string")
                re.compile(grammar)
                if re.fullmatch(grammar, ReconProbeConstants.SAMPLE_USERNAME) is None:
                    raise ValueError(f"GRAMMAR rejects probe username {ReconProbeConstants.SAMPLE_USERNAME!r}")

                probe_url = self._require_callable(module, "probe_url")(ReconProbeConstants.SAMPLE_USERNAME)
                self._require_https_url(probe_url, "probe_url")
                verdict = self._require_callable(module, "evaluate")(0, "", probe_url)
                if not isinstance(verdict, tuple) or len(verdict) != 2:
                    raise TypeError("evaluate must return a two-item tuple")
                if verdict[0] not in ReconProbeConstants.VALID_VERDICTS:
                    raise ValueError(f"evaluate returned invalid verdict: {verdict[0]!r}")
                if not isinstance(verdict[1], dict):
                    raise TypeError("evaluate info must be a dict")
                details.update({"grammar": grammar, "probe_url": probe_url, "empty_response_verdict": verdict[0]})

            result.status = "PASS"
            result.details = details
        except Exception as exc:
            result.reason = f"{type(exc).__name__}: {exc}"
            result.details = {"traceback": traceback.format_exc(limit=8)}
        result.elapsed_ms = round((time.monotonic() - started) * 1000)
        return result

    @staticmethod
    def _require_callable(owner: object, member_name: str) -> Callable[..., object]:
        member = getattr(owner, member_name, None)
        if member is None:
            raise AttributeError(f"{member_name} is missing or None")
        if not callable(member):
            raise TypeError(f"{member_name} is not callable")
        if not inspect.isfunction(member):
            raise TypeError(f"{member_name} must be a function")
        return member

    @staticmethod
    def _require_https_url(value: object, source: str) -> None:
        parsed = urlparse(str(value or ""))
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"{source} returned an invalid HTTPS URL: {value!r}")

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Validate every custom-recon platform probe in an isolated process.")
        parser.add_argument("--platform", action="append")
        parser.add_argument("--workers", type=int, default=4)
        parser.add_argument("--timeout", type=float, default=15.0)
        parser.add_argument("--output", type=Path)
        parser.add_argument("--worker", help=argparse.SUPPRESS)
        return parser
