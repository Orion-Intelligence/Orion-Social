from __future__ import annotations

import argparse
from pathlib import Path

from app.probe.recon_probe.email_probe import EmailProbe
from app.probe.recon_probe.name_probe import NameProbe
from app.probe.recon_probe.platform_probe import PlatformProbe


class ReconProbe:
    def invoke_probe(self, argv: list[str] | None = None) -> int:
        args = self._build_parser().parse_args(argv)
        output_dir = args.output_dir.expanduser().resolve() if args.output_dir else None
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)

        print("\n=== PLATFORM PROBE ===")
        platform_args = ["--workers", str(args.workers), "--timeout", str(args.platform_timeout)]
        if output_dir:
            platform_args.extend(["--output", str(output_dir / "platform_probe.json")])
        platform_status = PlatformProbe().invoke_probe(platform_args)

        print("\n=== EMAIL PROBE ===")
        email_args = ["--timeout", str(args.extractor_timeout)]
        if output_dir:
            email_args.extend(["--output", str(output_dir / "email_probe.json")])
        email_status = EmailProbe().invoke_probe(email_args)

        print("\n=== NAME PROBE ===")
        name_args = ["--timeout", str(args.extractor_timeout)]
        if output_dir:
            name_args.extend(["--output", str(output_dir / "name_probe.json")])
        name_status = NameProbe().invoke_probe(name_args)

        failed = sum(status != 0 for status in (platform_status, email_status, name_status))
        print(f"\nRECON PROBE SUMMARY groups=3 passed={3 - failed} failed={failed}")
        return 1 if failed else 0

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Run platform, email, and name contract probes.")
        parser.add_argument("--workers", type=int, default=4)
        parser.add_argument("--platform-timeout", type=float, default=15.0)
        parser.add_argument("--extractor-timeout", type=float, default=30.0)
        parser.add_argument("--output-dir", type=Path)
        return parser
