#!/usr/bin/env python3
"""
Audit Orion Social leak-style scraper scripts for loadability, API wiring, and
target-site reachability.

This is intentionally a lightweight checker. It imports scraper classes and
performs HTTP probes against configured site URLs, but it does not execute
parse_leak_data or collect content from those sites.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import inspect
import json
import socket
import ssl
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from types import ModuleType
from typing import Any
from urllib import error, request
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = REPO_ROOT / "app"
SCRAPER_DIR = APP_ROOT / "api" / "social_manager" / "scrapers"
ROUTES_PATH = APP_ROOT / "api" / "routes.py"
CONTROLLER_PATH = APP_ROOT / "api" / "social_manager" / "social_controller.py"

for candidate in (APP_ROOT, REPO_ROOT):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)


ROUTE_BY_CAPABILITY = {
    "profile": "/social/profile",
    "followers": "/social/followers",
    "following": "/social/following",
    "posts": "/social/posts",
    "videos": "/social/videos",
    "shorts": "/social/shorts",
}

FALLBACK_PROFILE_PLATFORMS = {
    "facebook",
    "instagram",
    "mastodon",
    "pastebin",
    "reddit",
    "tiktok",
    "twitter",
    "youtube",
}
FALLBACK_POST_PLATFORMS = {
    "facebook",
    "instagram",
    "mastodon",
    "pastebin",
    "reddit",
    "tiktok",
    "twitter",
    "youtube",
}
FALLBACK_FOLLOW_PLATFORMS = {"behance", "facebook", "instagram", "twitter", "vimeo"}

FALLBACK_SITE_URLS = {
    "behance": "https://www.behance.net",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "mastodon": "https://mastodon.social",
    "pastebin": "https://pastebin.com",
    "reddit": "https://www.reddit.com",
    "tiktok": "https://www.tiktok.com",
    "twitter": "https://x.com",
    "vimeo": "https://vimeo.com",
    "youtube": "https://www.youtube.com",
}


@dataclass
class HttpProbe:
    url: str
    state: str
    reachable: bool
    accessible: bool
    method: str = ""
    status_code: int | None = None
    final_url: str = ""
    elapsed_ms: int | None = None
    error: str = ""


@dataclass
class ScriptAudit:
    platform: str
    module_name: str
    file_path: str
    file_exists: bool
    import_ok: bool
    import_error: str
    class_name: str
    instantiate_ok: bool
    instantiate_error: str
    has_parse_leak_data: bool
    controller_lookup_ok: bool
    seed_url: str
    base_url: str
    api_capabilities: list[str]
    configured_fetch: str
    configured_proxy: str
    site_probe: HttpProbe | None
    base_probe: HttpProbe | None


def _safe_error(exc: BaseException) -> str:
    return f"{exc.__class__.__name__}: {exc}"


def _enum_value(value: Any) -> str:
    if value is None:
        return ""
    return str(getattr(value, "value", value))


def _load_social_platform_values() -> dict[str, str]:
    try:
        from api.social_manager.social_enums import SOCIAL_PLATFORMS
    except Exception:
        return {}

    values: dict[str, str] = {}
    for name, value in vars(SOCIAL_PLATFORMS).items():
        if name.isupper() and isinstance(value, str):
            values[name] = value
    return values


def _platform_from_ast(node: ast.AST, platform_values: dict[str, str]) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.strip().lower()
    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "SOCIAL_PLATFORMS"
    ):
        return platform_values.get(node.attr, node.attr.lower()).strip().lower()
    return None


def _extract_controller_platform_sets() -> dict[str, set[str]]:
    sets = {
        "profile": set(FALLBACK_PROFILE_PLATFORMS),
        "posts": set(FALLBACK_POST_PLATFORMS),
        "followers": set(FALLBACK_FOLLOW_PLATFORMS),
        "following": set(FALLBACK_FOLLOW_PLATFORMS),
    }
    if not CONTROLLER_PATH.exists():
        return sets

    platform_values = _load_social_platform_values()
    try:
        tree = ast.parse(CONTROLLER_PATH.read_text(encoding="utf-8"))
    except Exception:
        return sets

    target_names = {
        "supported_platforms": ("profile",),
        "native_platforms": ("posts",),
        "followers_following_supported_platforms": ("followers", "following"),
    }

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        matched_names = [name for name in names if name in target_names]
        if not matched_names or not isinstance(node.value, (ast.List, ast.Set, ast.Tuple)):
            continue
        platforms = {
            platform
            for item in node.value.elts
            if (platform := _platform_from_ast(item, platform_values))
        }
        if not platforms:
            continue
        for name in matched_names:
            for capability in target_names[name]:
                sets[capability] = set(platforms)

    return sets


def _extract_route_paths() -> set[str]:
    if not ROUTES_PATH.exists():
        return set()
    try:
        tree = ast.parse(ROUTES_PATH.read_text(encoding="utf-8"))
    except Exception:
        return set()

    paths: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute) or func.attr != "add_api_route":
            continue
        if not node.args:
            continue
        first_arg = node.args[0]
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            paths.add(first_arg.value)
    return paths


def _fetch_openapi_paths(api_base: str, timeout: float) -> tuple[set[str], str]:
    api_base = api_base.rstrip("/")
    if not api_base:
        return set(), ""
    url = f"{api_base}/openapi.json"
    probe = _http_json(url, timeout)
    if not isinstance(probe, dict):
        return set(), "openapi.json was not reachable or was not JSON"
    paths = probe.get("paths")
    if not isinstance(paths, dict):
        return set(), "openapi.json does not contain paths"
    return set(paths.keys()), ""


def _http_json(url: str, timeout: float) -> Any:
    headers = {"User-Agent": "Orion-Social-Leak-Script-Audit/1.0"}
    req = request.Request(url, headers=headers, method="GET")
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _class_names_for_platform(platform: str) -> list[str]:
    names = [f"_{platform}", f"{platform.capitalize()}Scraper"]
    if platform == "tiktok":
        names.append("TikTokScraper")
    return names


def _module_names_for_platform(platform: str) -> list[str]:
    return [
        f"api.social_manager.scrapers._{platform}",
        f"api.social_manager.scrapers.{platform}",
    ]


def _candidate_platforms() -> set[str]:
    platforms = set(FALLBACK_PROFILE_PLATFORMS)
    platforms.update(FALLBACK_POST_PLATFORMS)
    platforms.update(FALLBACK_FOLLOW_PLATFORMS)

    if SCRAPER_DIR.exists():
        for path in SCRAPER_DIR.glob("*.py"):
            if path.name == "__init__.py" or path.stem == "live_search_handler":
                continue
            platform = path.stem[1:] if path.stem.startswith("_") else path.stem
            platforms.add(platform.lower())
    return platforms


def _find_importable_module(platform: str) -> tuple[str, ModuleType | None, str]:
    last_error = ""
    for module_name in _module_names_for_platform(platform):
        try:
            return module_name, importlib.import_module(module_name), ""
        except ModuleNotFoundError as exc:
            if exc.name == module_name:
                last_error = _safe_error(exc)
                continue
            return module_name, None, _safe_error(exc)
        except Exception as exc:
            return module_name, None, _safe_error(exc)
    return _module_names_for_platform(platform)[0], None, last_error


def _find_scraper_class(platform: str, module: ModuleType | None) -> tuple[str, type[Any] | None]:
    if not module:
        return "", None

    for class_name in _class_names_for_platform(platform):
        candidate = getattr(module, class_name, None)
        if isinstance(candidate, type):
            return class_name, candidate

    for name, candidate in inspect.getmembers(module, inspect.isclass):
        if candidate.__module__ == module.__name__ and hasattr(candidate, "parse_leak_data"):
            return name, candidate

    return "", None


def _controller_lookup_ok(platform: str, module: ModuleType | None) -> bool:
    _, scraper_class = _find_scraper_class(platform, module)
    return scraper_class is not None


def _instantiate(scraper_class: type[Any] | None) -> tuple[Any | None, str]:
    if scraper_class is None:
        return None, "scraper class not found"
    try:
        return scraper_class(), ""
    except Exception as exc:
        return None, _safe_error(exc)


def _status_state(status_code: int | None, error_text: str = "") -> tuple[str, bool, bool]:
    if status_code is None:
        if error_text == "skipped":
            return "skipped", False, False
        return "error", False, False
    if 200 <= status_code < 400:
        return "accessible", True, True
    if status_code in {401, 403, 407, 429, 451}:
        return "reachable_blocked", True, False
    if 400 <= status_code < 500:
        return "reachable_not_accessible", True, False
    if 500 <= status_code < 600:
        return "reachable_server_error", True, False
    return "reachable_unknown", True, False


def _probe_url(url: str, timeout: float) -> HttpProbe:
    if not url:
        return HttpProbe(url="", state="skipped", reachable=False, accessible=False, error="no URL")

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return HttpProbe(url=url, state="skipped", reachable=False, accessible=False, error="not an HTTP URL")

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 Orion-Social-Leak-Script-Audit/1.0",
    }
    context = ssl.create_default_context()
    last_probe: HttpProbe | None = None

    for method in ("HEAD", "GET"):
        started = time.monotonic()
        req = request.Request(url, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=timeout, context=context) as resp:
                elapsed_ms = int((time.monotonic() - started) * 1000)
                state, reachable, accessible = _status_state(resp.status)
                return HttpProbe(
                    url=url,
                    state=state,
                    reachable=reachable,
                    accessible=accessible,
                    method=method,
                    status_code=resp.status,
                    final_url=resp.geturl(),
                    elapsed_ms=elapsed_ms,
                )
        except error.HTTPError as exc:
            elapsed_ms = int((time.monotonic() - started) * 1000)
            state, reachable, accessible = _status_state(exc.code)
            last_probe = HttpProbe(
                url=url,
                state=state,
                reachable=reachable,
                accessible=accessible,
                method=method,
                status_code=exc.code,
                final_url=exc.url or "",
                elapsed_ms=elapsed_ms,
                error=str(exc.reason),
            )
            if method == "HEAD":
                continue
            return last_probe
        except (error.URLError, TimeoutError, socket.timeout, ssl.SSLError, OSError) as exc:
            elapsed_ms = int((time.monotonic() - started) * 1000)
            last_probe = HttpProbe(
                url=url,
                state="error",
                reachable=False,
                accessible=False,
                method=method,
                elapsed_ms=elapsed_ms,
                error=_safe_error(exc),
            )
            if method == "HEAD":
                continue
            return last_probe

    return last_probe or HttpProbe(url=url, state="error", reachable=False, accessible=False, error="unknown")


def _api_capabilities(
    platform: str,
    route_paths: set[str],
    openapi_paths: set[str],
    controller_sets: dict[str, set[str]],
    script_lookup_ok: bool,
) -> list[str]:
    capabilities: list[str] = []
    available_paths = openapi_paths or route_paths

    for capability, route_path in ROUTE_BY_CAPABILITY.items():
        if route_path not in available_paths:
            continue
        if capability in {"videos", "shorts"}:
            if script_lookup_ok:
                capabilities.append(capability)
            continue
        if platform in controller_sets.get(capability, set()) and script_lookup_ok:
            capabilities.append(capability)
    return capabilities


def audit_platform(
    platform: str,
    route_paths: set[str],
    openapi_paths: set[str],
    controller_sets: dict[str, set[str]],
    do_network: bool,
    timeout: float,
    check_base_url: bool,
) -> ScriptAudit:
    file_candidates = [
        SCRAPER_DIR / f"_{platform}.py",
        SCRAPER_DIR / f"{platform}.py",
    ]
    file_path = next((path for path in file_candidates if path.exists()), file_candidates[0])
    module_name, module, import_error = _find_importable_module(platform)
    class_name, scraper_class = _find_scraper_class(platform, module)
    instance, instantiate_error = _instantiate(scraper_class)
    instantiate_ok = instance is not None and not instantiate_error
    import_ok = module is not None and not import_error
    has_parse = bool(scraper_class and hasattr(scraper_class, "parse_leak_data"))
    controller_lookup_ok = _controller_lookup_ok(platform, module)

    seed_url = ""
    base_url = ""
    configured_fetch = ""
    configured_proxy = ""

    if instance is not None:
        try:
            seed_url = str(getattr(instance, "seed_url", "") or "")
        except Exception as exc:
            seed_url = f"error: {_safe_error(exc)}"
        try:
            base_url = str(getattr(instance, "base_url", "") or "")
        except Exception as exc:
            base_url = f"error: {_safe_error(exc)}"
        try:
            rule_config = getattr(instance, "rule_config", None)
            configured_fetch = _enum_value(getattr(rule_config, "m_fetch_config", ""))
            configured_proxy = _enum_value(getattr(rule_config, "m_fetch_proxy", ""))
        except Exception as exc:
            configured_fetch = f"error: {_safe_error(exc)}"

    probe_url = seed_url if seed_url.startswith(("http://", "https://")) else FALLBACK_SITE_URLS.get(platform, "")
    base_probe_url = base_url if base_url.startswith(("http://", "https://")) else FALLBACK_SITE_URLS.get(platform, "")

    site_probe = _probe_url(probe_url, timeout) if do_network else HttpProbe(
        url=probe_url,
        state="skipped",
        reachable=False,
        accessible=False,
        error="network disabled",
    )
    base_probe = None
    if check_base_url:
        base_probe = _probe_url(base_probe_url, timeout) if do_network else HttpProbe(
            url=base_probe_url,
            state="skipped",
            reachable=False,
            accessible=False,
            error="network disabled",
        )

    return ScriptAudit(
        platform=platform,
        module_name=module_name,
        file_path=str(file_path.relative_to(REPO_ROOT)) if file_path.is_absolute() else str(file_path),
        file_exists=file_path.exists(),
        import_ok=import_ok,
        import_error=import_error,
        class_name=class_name,
        instantiate_ok=instantiate_ok,
        instantiate_error=instantiate_error,
        has_parse_leak_data=has_parse,
        controller_lookup_ok=controller_lookup_ok,
        seed_url=seed_url,
        base_url=base_url,
        api_capabilities=_api_capabilities(platform, route_paths, openapi_paths, controller_sets, controller_lookup_ok),
        configured_fetch=configured_fetch,
        configured_proxy=configured_proxy,
        site_probe=site_probe,
        base_probe=base_probe,
    )


def _script_state(audit: ScriptAudit) -> str:
    if not audit.file_exists:
        return "missing_file"
    if not audit.import_ok:
        return "import_error"
    if not audit.class_name:
        return "missing_class"
    if not audit.instantiate_ok:
        return "instantiation_error"
    if not audit.has_parse_leak_data:
        return "missing_parse"
    if not audit.controller_lookup_ok:
        return "not_wired"
    return "ok"


def _table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    columns = list(rows[0].keys())
    widths = {
        column: max(len(column), *(len(row.get(column, "")) for row in rows))
        for column in columns
    }
    header = "  ".join(column.ljust(widths[column]) for column in columns)
    divider = "  ".join("-" * widths[column] for column in columns)
    body = [
        "  ".join(row.get(column, "").ljust(widths[column]) for column in columns)
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def _format_probe(probe: HttpProbe | None) -> str:
    if probe is None:
        return "not_checked"
    if probe.status_code is not None:
        return f"{probe.state}:{probe.status_code}"
    return probe.state


def _print_text(audits: list[ScriptAudit], api_error: str) -> None:
    rows: list[dict[str, str]] = []
    for audit in audits:
        rows.append(
            {
                "platform": audit.platform,
                "script": _script_state(audit),
                "class": audit.class_name or "-",
                "api": ",".join(audit.api_capabilities) or "-",
                "site": _format_probe(audit.site_probe),
                "base": _format_probe(audit.base_probe),
                "url": (audit.site_probe.url if audit.site_probe else audit.seed_url) or "-",
            }
        )

    print(_table(rows))
    if api_error:
        print(f"\nAPI check warning: {api_error}")

    total = len(audits)
    script_ok = sum(1 for audit in audits if _script_state(audit) == "ok")
    accessible = sum(1 for audit in audits if audit.site_probe and audit.site_probe.accessible)
    reachable = sum(1 for audit in audits if audit.site_probe and audit.site_probe.reachable)
    print(
        f"\nSummary: scripts ok {script_ok}/{total}; "
        f"site accessible {accessible}/{total}; site reachable {reachable}/{total}"
    )

    failed = [
        audit
        for audit in audits
        if _script_state(audit) != "ok"
        or (audit.site_probe and audit.site_probe.state not in {"accessible", "skipped"})
    ]
    if failed:
        print("\nDetails for non-OK entries:")
        for audit in failed:
            script_state = _script_state(audit)
            reasons: list[str] = []
            if audit.import_error:
                reasons.append(audit.import_error)
            if audit.instantiate_error and script_state == "instantiation_error":
                reasons.append(audit.instantiate_error)
            if audit.site_probe and audit.site_probe.error and audit.site_probe.state != "skipped":
                reasons.append(f"site {audit.site_probe.error}")
            reason_text = f" ({'; '.join(reasons)})" if reasons else ""
            print(f"- {audit.platform}: {script_state}, site={_format_probe(audit.site_probe)}{reason_text}")


def _json_ready(audits: list[ScriptAudit], api_error: str) -> dict[str, Any]:
    return {
        "api_error": api_error,
        "audits": [
            {
                **asdict(audit),
                "script_state": _script_state(audit),
            }
            for audit in audits
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check which Orion Social leak-style scraper scripts are loadable and site-reachable."
    )
    parser.add_argument(
        "--platform",
        action="append",
        help="Limit the audit to one platform. Can be passed more than once.",
    )
    parser.add_argument(
        "--no-network",
        action="store_true",
        help="Skip target-site HTTP reachability checks.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=8.0,
        help="HTTP timeout in seconds for each reachability probe.",
    )
    parser.add_argument(
        "--api-base",
        default="",
        help="Optional running API base URL, e.g. http://localhost:8020. Checks /openapi.json routes.",
    )
    parser.add_argument(
        "--check-base-url",
        action="store_true",
        help="Also probe each scraper base_url in addition to its seed_url.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a table.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with status 1 when a script is not OK or a network probe is not accessible.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    route_paths = _extract_route_paths()
    openapi_paths: set[str] = set()
    api_error = ""
    if args.api_base:
        try:
            openapi_paths, api_error = _fetch_openapi_paths(args.api_base, args.timeout)
        except Exception as exc:
            api_error = _safe_error(exc)

    controller_sets = _extract_controller_platform_sets()
    selected_platforms = {platform.lower().strip() for platform in args.platform or [] if platform.strip()}
    platforms = selected_platforms or _candidate_platforms()

    audits = [
        audit_platform(
            platform=platform,
            route_paths=route_paths,
            openapi_paths=openapi_paths,
            controller_sets=controller_sets,
            do_network=not args.no_network,
            timeout=args.timeout,
            check_base_url=args.check_base_url,
        )
        for platform in sorted(platforms)
    ]

    if args.json:
        print(json.dumps(_json_ready(audits, api_error), indent=2, sort_keys=True))
    else:
        _print_text(audits, api_error)

    if args.strict:
        for audit in audits:
            if _script_state(audit) != "ok":
                return 1
            if audit.site_probe and not audit.site_probe.accessible:
                return 1
            if audit.base_probe and not audit.base_probe.accessible:
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
