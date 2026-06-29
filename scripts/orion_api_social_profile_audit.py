#!/usr/bin/env python3
"""
Exercise Orion Social through the public HTTP API.

The script posts to /social/profile or /social/posts, polls the same payload
until the Orion job returns a result, and validates returned cards for platform,
expected content type, image fields, and empty/timeout/error states.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib import error, request


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ApiCase:
    platform: str
    username: str
    kind: str = "profile"


@dataclass
class ApiResult:
    platform: str
    username: str
    kind: str
    status: str
    elapsed_ms: int
    job_id: str = ""
    polls: int = 0
    http_status: int | None = None
    error: str = ""
    cards_count: int = 0
    profile_cards: int = 0
    post_cards: int = 0
    returned_posts: bool = False
    has_profile_image: bool = False
    has_cover_image: bool = False
    wrong_platform: bool = False
    scraper_files: list[str] | None = None
    sample_cards: list[dict[str, Any]] | None = None
    last_response: dict[str, Any] | None = None


CASES: list[ApiCase] = [
    ApiCase("facebook", "https://www.facebook.com/nasa", "page"),
    ApiCase("facebook", "https://www.facebook.com/meta", "page"),
    ApiCase("facebook", "https://www.facebook.com/bbcnews", "page"),
    ApiCase("facebook", "https://www.facebook.com/olympics", "page"),
    ApiCase("facebook", "https://www.facebook.com/cocacola", "page"),
    ApiCase("instagram", "https://www.instagram.com/nasa/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/natgeo/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/openai/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/github/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/nike/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/google/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/microsoft/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/adobe/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/spotify/", "profile"),
    ApiCase("instagram", "https://www.instagram.com/netflix/", "profile"),
    ApiCase("linkedin", "https://www.linkedin.com/company/openai/", "company"),
    ApiCase("linkedin", "https://www.linkedin.com/company/microsoft/", "company"),
    ApiCase("linkedin", "https://www.linkedin.com/company/google/", "company"),
    ApiCase("linkedin", "https://www.linkedin.com/in/bkrebs/", "profile"),
    ApiCase("linkedin", "https://www.linkedin.com/in/reidhoffman/", "profile"),
    ApiCase("mastodon", "https://mastodon.social/@staff", "profile"),
    ApiCase("mastodon", "https://infosec.exchange/@malwaretech", "profile"),
    ApiCase("mastodon", "https://fosstodon.org/@fosstodon", "profile"),
    ApiCase("mastodon", "https://mastodon.social/@Tusky", "profile"),
    ApiCase("mastodon", "https://floss.social/@kde", "profile"),
    ApiCase("pastebin", "https://pastebin.com/pW3xDnhk", "paste"),
    ApiCase("pastebin", "https://pastebin.com/CMu7baEY", "paste"),
    ApiCase("pastebin", "https://pastebin.com/jJXaneCA", "paste"),
    ApiCase("pastebin", "https://pastebin.com/wpbdrLbc", "paste"),
    ApiCase("pastebin", "https://pastebin.com/NQvucZUz", "paste"),
    ApiCase("reddit", "https://www.reddit.com/r/coding/", "subreddit"),
    ApiCase("reddit", "https://www.reddit.com/r/sysadmin/", "subreddit"),
    ApiCase("reddit", "https://www.reddit.com/r/homelab/", "subreddit"),
    ApiCase("reddit", "https://www.reddit.com/r/learnpython/", "subreddit"),
    ApiCase("reddit", "https://www.reddit.com/r/rust/", "subreddit"),
    ApiCase("tiktok", "https://www.tiktok.com/@f1", "profile"),
    ApiCase("tiktok", "https://www.tiktok.com/@nfl", "profile"),
    ApiCase("tiktok", "https://www.tiktok.com/@mlb", "profile"),
    ApiCase("tiktok", "https://www.tiktok.com/@lego", "profile"),
    ApiCase("tiktok", "https://www.tiktok.com/@nike", "profile"),
    ApiCase("twitter", "https://x.com/amazon", "profile"),
    ApiCase("twitter", "https://x.com/nvidia", "profile"),
    ApiCase("twitter", "https://x.com/adobe", "profile"),
    ApiCase("twitter", "https://x.com/un", "profile"),
    ApiCase("twitter", "https://x.com/salesforce", "profile"),
    ApiCase("youtube", "https://www.youtube.com/@microsoft", "channel"),
    ApiCase("youtube", "https://www.youtube.com/@adobecreativecloud", "channel"),
    ApiCase("youtube", "https://www.youtube.com/@netflix", "channel"),
    ApiCase("youtube", "https://www.youtube.com/@spotify", "channel"),
    ApiCase("youtube", "https://www.youtube.com/@redbull", "channel"),
]


def _safe_error(exc: BaseException) -> str:
    return f"{exc.__class__.__name__}: {exc}"


def _post_json(api_base: str, path: str, payload: dict[str, Any], timeout: float) -> tuple[int, dict[str, Any]]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{api_base.rstrip('/')}{path}",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Orion-Social-API-Audit/1.0",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")
        return response.status, json.loads(text or "{}")


def _get_json(api_base: str, path: str, timeout: float) -> tuple[int, dict[str, Any]]:
    req = request.Request(
        f"{api_base.rstrip('/')}{path}",
        headers={"Accept": "application/json", "User-Agent": "Orion-Social-API-Audit/1.0"},
        method="GET",
    )
    with request.urlopen(req, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")
        return response.status, json.loads(text or "{}")


def _content_types(card: dict[str, Any]) -> list[str]:
    return [str(item).lower() for item in (card.get("m_content_type") or [])]


def _is_profile_card(card: dict[str, Any]) -> bool:
    return any("profile" in item or "channel_info" in item for item in _content_types(card))


def _is_post_card(card: dict[str, Any]) -> bool:
    content_types = _content_types(card)
    if not content_types or _is_profile_card(card):
        return False
    return any(
        item == "posts"
        or item == "videos"
        or item == "shorts"
        or "post" in item
        or "video" in item
        or "short" in item
        for item in content_types
    )


def _sample_card(card: dict[str, Any]) -> dict[str, Any]:
    content = str(card.get("m_content") or "")
    if len(content) > 180:
        content = f"{content[:180]}..."
    return {
        "m_scrap_file": card.get("m_scrap_file"),
        "m_platform": card.get("m_platform"),
        "m_title": card.get("m_title"),
        "m_url": card.get("m_url"),
        "m_content_type": card.get("m_content_type"),
        "m_img_src": card.get("m_img_src"),
        "m_coverpage": card.get("m_coverpage"),
        "m_content_preview": content,
    }


def _normalize_cards(response: dict[str, Any]) -> list[dict[str, Any]]:
    result = response.get("result")
    if isinstance(result, list):
        return [item for item in result if isinstance(item, dict)]
    if isinstance(result, dict):
        data = result.get("data")
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
    return []


def _classify(case: ApiCase, response: dict[str, Any], elapsed_ms: int, polls: int, http_status: int | None, endpoint: str) -> ApiResult:
    cards = _normalize_cards(response)
    profile_cards = [card for card in cards if _is_profile_card(card)]
    post_cards = [card for card in cards if _is_post_card(card)]
    checked_cards = profile_cards if endpoint == "profile" else post_cards
    checked_cards = checked_cards or cards
    wrong_platform = any(
        str(card.get("m_platform") or "").lower() not in {"", case.platform}
        for card in checked_cards
    )
    has_profile_image = any(bool(card.get("m_img_src")) for card in checked_cards)
    has_cover_image = any(bool(card.get("m_coverpage")) for card in checked_cards)
    status = "ok"
    if not cards:
        status = "no_data"
    elif wrong_platform:
        status = "wrong_platform"
    elif endpoint == "profile" and not profile_cards:
        status = "no_profile_card"
    elif endpoint == "profile" and not has_profile_image:
        status = "profile_image_missing"
    elif endpoint == "posts" and not post_cards:
        status = "no_post_card"

    return ApiResult(
        platform=case.platform,
        username=case.username,
        kind=case.kind,
        status=status,
        elapsed_ms=elapsed_ms,
        job_id=str(response.get("job_id") or ""),
        polls=polls,
        http_status=http_status,
        cards_count=len(cards),
        profile_cards=len(profile_cards),
        post_cards=len(post_cards),
        returned_posts=bool(post_cards),
        has_profile_image=has_profile_image,
        has_cover_image=has_cover_image,
        wrong_platform=wrong_platform,
        scraper_files=sorted({str(card.get("m_scrap_file") or "") for card in checked_cards if card.get("m_scrap_file")}),
        sample_cards=[_sample_card(card) for card in checked_cards[:2]],
        last_response=response if status != "ok" else None,
    )


def run_case(
    case: ApiCase,
    api_base: str,
    endpoint: str,
    request_timeout: float,
    case_timeout: float,
    poll_interval: float,
    max_posts: int,
    max_comments: int,
) -> ApiResult:
    started = time.monotonic()
    if endpoint == "posts":
        path = "/social/posts"
        payload = {
            "platform": case.platform,
            "username": case.username,
            "max_posts": max_posts,
            "max_comments": max_comments,
            "comment_offset": 0,
            "social_data_type": "posts",
        }
    else:
        path = "/social/profile"
        payload = {
            "platform": case.platform,
            "username": case.username,
            "social_data_type": "profile_info",
        }
    polls = 0
    http_status: int | None = None
    last_response: dict[str, Any] = {}
    while True:
        elapsed = time.monotonic() - started
        if elapsed > case_timeout:
            return ApiResult(
                platform=case.platform,
                username=case.username,
                kind=case.kind,
                status="timeout",
                elapsed_ms=int(elapsed * 1000),
                polls=polls,
                http_status=http_status,
                error=f"API job did not finish within {case_timeout:.1f}s",
                last_response=last_response or None,
            )
        polls += 1
        try:
            http_status, last_response = _post_json(api_base, path, payload, request_timeout)
        except error.HTTPError as exc:
            try:
                body = exc.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            return ApiResult(
                platform=case.platform,
                username=case.username,
                kind=case.kind,
                status="http_error",
                elapsed_ms=int((time.monotonic() - started) * 1000),
                polls=polls,
                http_status=exc.code,
                error=f"{exc.reason}: {body[:500]}",
            )
        except Exception as exc:
            return ApiResult(
                platform=case.platform,
                username=case.username,
                kind=case.kind,
                status="request_error",
                elapsed_ms=int((time.monotonic() - started) * 1000),
                polls=polls,
                http_status=http_status,
                error=_safe_error(exc),
            )

        if last_response.get("status") == "error":
            return ApiResult(
                platform=case.platform,
                username=case.username,
                kind=case.kind,
                status="api_error",
                elapsed_ms=int((time.monotonic() - started) * 1000),
                job_id=str(last_response.get("job_id") or ""),
                polls=polls,
                http_status=http_status,
                error=str(last_response.get("message") or last_response),
                last_response=last_response,
            )
        if "result" in last_response:
            return _classify(case, last_response, int((time.monotonic() - started) * 1000), polls, http_status, endpoint)
        time.sleep(poll_interval)


def _selected_cases(platforms: set[str], limit_per_platform: int) -> list[ApiCase]:
    counts: dict[str, int] = {}
    selected: list[ApiCase] = []
    for case in CASES:
        if platforms and case.platform not in platforms:
            continue
        count = counts.get(case.platform, 0)
        if count >= limit_per_platform:
            continue
        selected.append(case)
        counts[case.platform] = count + 1
    return selected


def _summary(results: list[ApiResult]) -> dict[str, Any]:
    platforms = sorted({result.platform for result in results})
    return {
        "total_cases": len(results),
        "ok_cases": sum(1 for result in results if result.status == "ok"),
        "timeout_cases": sum(1 for result in results if result.status == "timeout"),
        "error_cases": sum(1 for result in results if result.status not in {"ok"}),
        "returned_posts_cases": sum(1 for result in results if result.returned_posts),
        "profile_image_cases": sum(1 for result in results if result.has_profile_image),
        "cover_image_cases": sum(1 for result in results if result.has_cover_image),
        "by_platform": {
            platform: {
                "cases": len(rows := [result for result in results if result.platform == platform]),
                "ok_cases": sum(1 for row in rows if row.status == "ok"),
                "returned_posts_cases": sum(1 for row in rows if row.returned_posts),
                "profile_image_cases": sum(1 for row in rows if row.has_profile_image),
                "cover_image_cases": sum(1 for row in rows if row.has_cover_image),
                "statuses": {
                    status: sum(1 for row in rows if row.status == status)
                    for status in sorted({row.status for row in rows})
                },
            }
            for platform in platforms
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-base", default="http://127.0.0.1:8020")
    parser.add_argument("--endpoint", choices=["profile", "posts"], default="profile")
    parser.add_argument("--platform", action="append", help="Limit to one platform. Can be repeated.")
    parser.add_argument("--limit-per-platform", type=int, default=3)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--max-posts", type=int, default=2)
    parser.add_argument("--max-comments", type=int, default=2)
    parser.add_argument("--request-timeout", type=float, default=30)
    parser.add_argument("--case-timeout", type=float, default=90)
    parser.add_argument("--poll-interval", type=float, default=2)
    parser.add_argument("--output", default="")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    platforms = {platform.strip().lower() for platform in args.platform or [] if platform.strip()}
    cases = _selected_cases(platforms, args.limit_per_platform)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_path = Path(args.output) if args.output else Path("/tmp") / f"orion_api_social_profile_audit_{timestamp}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        _, openapi = _get_json(args.api_base, "/openapi.json", args.request_timeout)
        paths = set((openapi.get("paths") or {}).keys())
        route_path = f"/social/{args.endpoint}"
        if route_path not in paths:
            raise RuntimeError(f"{route_path} is not present in openapi.json")
    except Exception as exc:
        print(f"API preflight failed: {_safe_error(exc)}", file=sys.stderr)
        return 2

    results: list[ApiResult] = []
    max_workers = max(1, min(int(args.concurrency or 1), 8))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(
                run_case,
                case,
                args.api_base,
                args.endpoint,
                args.request_timeout,
                args.case_timeout,
                args.poll_interval,
                args.max_posts,
                args.max_comments,
            ): case
            for case in cases
        }
        for index, future in enumerate(concurrent.futures.as_completed(future_map), start=1):
            case = future_map[future]
            try:
                result = future.result()
            except Exception as exc:
                result = ApiResult(
                    platform=case.platform,
                    username=case.username,
                    kind=case.kind,
                    status="runner_error",
                    elapsed_ms=0,
                    error=_safe_error(exc),
                )
            results.append(result)
            print(
                f"[{index:02d}/{len(cases):02d}] {result.platform:<9} "
                f"status={result.status:<22} cards={result.cards_count:<2} "
                f"posts={result.post_cards:<2} profile_img={result.has_profile_image} cover_img={result.has_cover_image} "
                f"elapsed_ms={result.elapsed_ms} {result.username}",
                flush=True,
            )

            report = {
                "generated_at": timestamp,
                "api_base": args.api_base,
                "settings": {
                    "endpoint": args.endpoint,
                    "limit_per_platform": args.limit_per_platform,
                    "concurrency": max_workers,
                    "max_posts": args.max_posts,
                    "max_comments": args.max_comments,
                    "request_timeout": args.request_timeout,
                    "case_timeout": args.case_timeout,
                    "poll_interval": args.poll_interval,
                },
                "cases": [asdict(case) for case in cases],
                "results": [asdict(row) for row in sorted(results, key=lambda item: (item.platform, item.username))],
                "summary": _summary(results),
            }
            output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    print(f"report={output_path}", flush=True)
    print(json.dumps(_summary(results), indent=2, sort_keys=True), flush=True)
    return 1 if any(result.status not in {"ok"} for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
