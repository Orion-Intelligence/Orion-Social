from __future__ import annotations

import argparse
import importlib
import inspect
import re
import sys
import time
import traceback
from pathlib import Path

from app.probe.recon_probe.constant.recon_probe_constant import ReconProbeConstants
from app.probe.recon_probe.model.recon_probe_model import ProbeResult
from app.probe.recon_probe.probe_base import _ProbeBase


class NameProbe(_ProbeBase):
    def invoke_probe(self, argv: list[str] | None = None) -> int:
        args = self._build_parser().parse_args(argv)
        if args.worker:
            return self._emit_worker_result(self._probe_worker(args.username))

        timeout = args.timeout if args.timeout is not None else (560.0 if args.username else 30.0)
        if timeout <= 0:
            raise SystemExit("--timeout must be greater than zero")
        worker_args = ["--worker"]
        if args.username:
            worker_args.extend(["--username", args.username])
        mode = args.username or "contract"
        print(f"Probing name extractor; mode={mode}; timeout={timeout:g}s", flush=True)
        result = self._run_worker(ReconProbeConstants.NAME_SCRIPT_MODULE, worker_args, "name", mode, timeout)
        self._print_result(1, 1, result)
        return self._finish_results([result], args.output)

    def _probe_worker(self, username: str | None) -> ProbeResult:
        started = time.monotonic()
        target = username or "contract"
        result = ProbeResult("name", target, "ERROR", 0)
        try:
            self._configure_import_paths()
            module = importlib.import_module(ReconProbeConstants.NAME_MODULE)
            extractor_class = getattr(module, "username_extractor", None)
            if not inspect.isclass(extractor_class):
                raise TypeError("username_extractor is missing or is not a class")
            extract = getattr(extractor_class, "extract", None)
            load_database = getattr(extractor_class, "_load_database", None)
            if not callable(extract):
                raise TypeError("username_extractor.extract is missing or not callable")
            if not callable(load_database):
                raise TypeError("username_extractor._load_database is missing or not callable")

            database = load_database()
            ranked_sites = database.ranked_sites_dict(top=sys.maxsize, disabled=False, id_type="username")
            if not isinstance(ranked_sites, dict) or not ranked_sites:
                raise ValueError("Maigret username database contains no enabled sites")

            if username:
                if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", username) is None:
                    raise ValueError("--username must contain only letters, numbers, dot, underscore, or hyphen")
                extracted = extract(username)
                if not isinstance(extracted, list):
                    raise TypeError("username_extractor.extract must return a list")
                platforms = [str((item.get("metadata") or {}).get("platform") or "") for item in extracted if isinstance(item, dict)]
                details = {"module": ReconProbeConstants.NAME_MODULE, "mode": "live", "maigret_sites": len(ranked_sites), "result_count": len(extracted), "platforms": [platform for platform in platforms if platform]}
            else:
                extracted = extract("")
                if extracted != []:
                    raise ValueError(f"empty username must return an empty list, received {extracted!r}")
                constant_class = getattr(module, "UsernameExtractorConstants", None)
                if not inspect.isclass(constant_class):
                    raise TypeError("UsernameExtractorConstants is missing or is not a class")
                site_timeout = constant_class.SITE_TIMEOUT
                search_deadline = constant_class.SEARCH_DEADLINE
                if not isinstance(site_timeout, int) or site_timeout <= 0:
                    raise ValueError("SITE_TIMEOUT must be a positive integer")
                if not isinstance(search_deadline, int) or search_deadline <= site_timeout:
                    raise ValueError("SEARCH_DEADLINE must be greater than SITE_TIMEOUT")
                details = {"module": ReconProbeConstants.NAME_MODULE, "mode": "contract", "maigret_sites": len(ranked_sites), "site_timeout": site_timeout, "search_deadline": search_deadline}

            result.status = "PASS"
            result.details = details
        except Exception as exc:
            result.reason = f"{type(exc).__name__}: {exc}"
            result.details = {"traceback": traceback.format_exc(limit=8)}
        result.elapsed_ms = round((time.monotonic() - started) * 1000)
        return result

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Validate the Maigret name extractor contract or run a live username probe.")
        parser.add_argument("--username")
        parser.add_argument("--timeout", type=float)
        parser.add_argument("--output", type=Path)
        parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
        return parser
