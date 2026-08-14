from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path

from app.probe.recon_probe.constant.recon_probe_constant import ReconProbeConstants
from app.probe.recon_probe.model.recon_probe_model import ProbeResult


class _ProbeBase:
    @staticmethod
    def _configure_import_paths() -> None:
        for path in (ReconProbeConstants.REPOSITORY_ROOT, ReconProbeConstants.APPLICATION_ROOT):
            value = str(path)
            if value not in sys.path:
                sys.path.insert(0, value)

    @staticmethod
    def _emit_worker_result(result: ProbeResult) -> int:
        print(ReconProbeConstants.RESULT_PREFIX + json.dumps(asdict(result), default=str, sort_keys=True))
        return 0 if result.status == "PASS" else 1

    @staticmethod
    def _terminate_worker(process: subprocess.Popen[str]) -> tuple[str, str]:
        if process.poll() is None:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGTERM)
            else:
                process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            stdout, stderr = process.communicate()
        return stdout or "", stderr or ""

    def _run_worker(self, script_module: str, worker_args: list[str], probe: str, target: str, timeout_seconds: float) -> ProbeResult:
        started = time.monotonic()
        environment = dict(os.environ)
        import_paths = [str(ReconProbeConstants.APPLICATION_ROOT), str(ReconProbeConstants.REPOSITORY_ROOT)]
        if environment.get("PYTHONPATH"):
            import_paths.append(environment["PYTHONPATH"])
        environment["PYTHONPATH"] = os.pathsep.join(import_paths)
        process = subprocess.Popen(
            [sys.executable, "-m", script_module, *worker_args],
            cwd=ReconProbeConstants.REPOSITORY_ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=os.name == "posix",
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout_seconds)
            stdout = stdout or ""
            stderr = stderr or ""
        except subprocess.TimeoutExpired:
            stdout, stderr = self._terminate_worker(process)
            return ProbeResult(
                probe=probe,
                target=target,
                status="TIMEOUT",
                elapsed_ms=round((time.monotonic() - started) * 1000),
                reason=f"exceeded {timeout_seconds:g} seconds",
                details={"stdout": stdout[-2000:], "stderr": stderr[-4000:]},
            )

        payload = next(
            (
                line[len(ReconProbeConstants.RESULT_PREFIX) :]
                for line in reversed(stdout.splitlines())
                if line.startswith(ReconProbeConstants.RESULT_PREFIX)
            ),
            None,
        )
        if payload is None:
            return ProbeResult(
                probe=probe,
                target=target,
                status="ERROR",
                elapsed_ms=round((time.monotonic() - started) * 1000),
                reason=f"worker exited {process.returncode} without a result",
                details={"stdout": stdout[-2000:], "stderr": stderr[-4000:]},
            )
        try:
            result = ProbeResult(**json.loads(payload))
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            return ProbeResult(
                probe=probe,
                target=target,
                status="ERROR",
                elapsed_ms=round((time.monotonic() - started) * 1000),
                reason=f"invalid worker result: {exc}",
                details={"payload": payload[-4000:], "stderr": stderr[-4000:]},
            )
        if process.returncode != 0 and result.status == "PASS":
            result.status = "ERROR"
            result.reason = f"worker exited {process.returncode}"
        return result

    @staticmethod
    def _print_result(index: int, total: int, result: ProbeResult) -> None:
        name = f"{result.probe}/{result.target}"
        suffix = f" {result.reason}" if result.reason else ""
        print(f"[{index:03d}/{total:03d}] {name:<48} {result.status:<7} {result.elapsed_ms:>6}ms{suffix}", flush=True)

    @staticmethod
    def _print_group(title: str, results: list[ProbeResult]) -> None:
        print(f"\n{title} ({len(results)})")
        if not results:
            print("  none")
            return
        for result in sorted(results, key=lambda item: (item.probe, item.target)):
            suffix = f" - {result.reason}" if result.reason else ""
            print(f"  {result.probe}/{result.target}{suffix}")

    def _finish_results(self, results: list[ProbeResult], output_path: Path | None = None) -> int:
        results = sorted(results, key=lambda item: (item.probe, item.target))
        passed = [result for result in results if result.status == "PASS"]
        errors = [result for result in results if result.status == "ERROR"]
        timeouts = [result for result in results if result.status == "TIMEOUT"]
        self._print_group("RUNNING", passed)
        self._print_group("ERRORS", errors)
        self._print_group("TIMEOUTS", timeouts)
        print(f"\nSUMMARY total={len(results)} running={len(passed)} errors={len(errors)} timeouts={len(timeouts)}", flush=True)
        if output_path:
            self._write_output(output_path, results, passed, errors, timeouts)
        return 1 if errors or timeouts else 0

    @staticmethod
    def _write_output(output_path: Path, results: list[ProbeResult], passed: list[ProbeResult], errors: list[ProbeResult], timeouts: list[ProbeResult]) -> None:
        output = output_path.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(
                {
                    "summary": {
                        "total": len(results),
                        "running": len(passed),
                        "errors": len(errors),
                        "timeouts": len(timeouts),
                    },
                    "results": [asdict(result) for result in results],
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"Results written to {output}")
