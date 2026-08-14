from __future__ import annotations

import argparse
import importlib
import inspect
import re
import shutil
import sys
import time
import traceback
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from app.probe.recon_probe.constant.recon_probe_constant import ReconProbeConstants
from app.probe.recon_probe.model.recon_probe_model import ProbeResult
from app.probe.recon_probe.probe_base import _ProbeBase


class EmailProbe(_ProbeBase):
    def invoke_probe(self, argv: list[str] | None = None) -> int:
        args = self._build_parser().parse_args(argv)
        if args.worker:
            return self._emit_worker_result(self._probe_worker(args.email))

        timeout = args.timeout if args.timeout is not None else (130.0 if args.email else 30.0)
        if timeout <= 0:
            raise SystemExit("--timeout must be greater than zero")
        worker_args = ["--worker"]
        if args.email:
            worker_args.extend(["--email", args.email])
        mode = args.email or "contract"
        print(f"Probing email extractor; mode={mode}; timeout={timeout:g}s", flush=True)
        result = self._run_worker(ReconProbeConstants.EMAIL_SCRIPT_MODULE, worker_args, "email", mode, timeout)
        self._print_result(1, 1, result)
        return self._finish_results([result], args.output)

    def _probe_worker(self, email: str | None) -> ProbeResult:
        started = time.monotonic()
        target = email or "contract"
        result = ProbeResult("email", target, "ERROR", 0)
        try:
            self._configure_import_paths()
            module = importlib.import_module(ReconProbeConstants.EMAIL_MODULE)
            extractor_class = getattr(module, "email_extractor", None)
            if not inspect.isclass(extractor_class):
                raise TypeError("email_extractor is missing or is not a class")
            extract = getattr(extractor_class, "extract", None)
            if not callable(extract):
                raise TypeError("email_extractor.extract is missing or not callable")
            constant_class = getattr(module, "EmailExtractorConstants", None)
            if not inspect.isclass(constant_class):
                raise TypeError("EmailExtractorConstants is missing or is not a class")
            if not isinstance(constant_class.HOLEHE_TIMEOUT, int) or constant_class.HOLEHE_TIMEOUT <= 0:
                raise ValueError("HOLEHE_TIMEOUT must be a positive integer")

            executable = shutil.which("holehe")
            sibling_executable = Path(sys.executable).resolve().parent / "holehe"
            if executable is None and sibling_executable.is_file():
                executable = str(sibling_executable)
            if executable is None:
                raise FileNotFoundError("holehe executable is not available")

            if email:
                if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is None:
                    raise ValueError("--email must be a valid email address")
                extracted = extract(email)
                if not isinstance(extracted, dict) or not isinstance(extracted.get("found"), list):
                    raise TypeError("email_extractor.extract must return {'found': list}")
                details = {"module": ReconProbeConstants.EMAIL_MODULE, "mode": "live", "holehe": executable, "found_count": len(extracted["found"])}
            else:
                original_run = module.subprocess.run

                def fake_run(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
                    return SimpleNamespace(stdout="[+] GitHub: registered\n[+] Gravatar: https://gravatar.com/orionprobe\n[-] ignored", stderr="", returncode=0)

                try:
                    module.subprocess.run = fake_run
                    extracted = extract("probe@example.com")
                finally:
                    module.subprocess.run = original_run
                expected = [
                    {"service": "GitHub", "result": "registered"},
                    {"service": "Gravatar", "result": "https://gravatar.com/orionprobe"},
                ]
                if extracted != {"found": expected}:
                    raise ValueError(f"unexpected parser result: {extracted!r}")
                details = {"module": ReconProbeConstants.EMAIL_MODULE, "mode": "contract", "holehe": executable, "parsed_services": [item["service"] for item in expected]}

            result.status = "PASS"
            result.details = details
        except Exception as exc:
            result.reason = f"{type(exc).__name__}: {exc}"
            result.details = {"traceback": traceback.format_exc(limit=8)}
        result.elapsed_ms = round((time.monotonic() - started) * 1000)
        return result

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Validate the email extractor contract or run a live email probe.")
        parser.add_argument("--email")
        parser.add_argument("--timeout", type=float)
        parser.add_argument("--output", type=Path)
        parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
        return parser
