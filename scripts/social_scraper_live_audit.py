#!/usr/bin/env python3
"""
Run live post-return checks for the underscore social scrapers.

The audit uses ten real profile/page handles per platform. For each case it:
1. opens the public profile/page URL in Playwright,
2. calls the scraper's parse_leak_data method with a small item limit,
3. records whether post-like cards were returned.

This script is intentionally diagnostic. It does not modify scraper behavior.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import signal
import subprocess
import sys
import time
import traceback
from dataclasses import asdict, dataclass
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = REPO_ROOT / "app"

for candidate in (REPO_ROOT, APP_ROOT):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from crawler.crawler_instance.local_shared_model.rule_model import SocialDataType  # noqa: E402


@dataclass(frozen=True)
class ScraperSpec:
    platform: str
    module_name: str
    class_name: str
    data_type: SocialDataType
    notes: str = ""


@dataclass(frozen=True)
class AuditCase:
    platform: str
    username: str
    profile_url: str
    kind: str = "profile"


@dataclass
class CaseResult:
    platform: str
    username: str
    profile_url: str
    kind: str
    data_type: str
    status: str
    returned_posts: bool
    total_cards: int
    post_cards: int
    profile_cards: int
    elapsed_ms: int
    final_url: str = ""
    goto_error: str = ""
    parse_error: str = ""
    scraper_status: str = ""
    scraper_reason: str = ""
    page_state: dict[str, Any] | None = None
    has_profile_image: bool = False
    has_cover_image: bool = False
    profile_image_url: str = ""
    cover_image_url: str = ""
    sample_cards: list[dict[str, Any]] | None = None


SCRAPERS: dict[str, ScraperSpec] = {
    "facebook": ScraperSpec(
        "facebook",
        "app.api.social_manager.scrapers._facebook",
        "_facebook",
        SocialDataType.POSTS,
        "Public Facebook pages often require a saved session before posts are visible.",
    ),
    "instagram": ScraperSpec(
        "instagram",
        "app.api.social_manager.scrapers._instagram",
        "_instagram",
        SocialDataType.POSTS,
        "Public Instagram profiles may show a login wall without a saved session.",
    ),
    "linkedin": ScraperSpec(
        "linkedin",
        "app.api.social_manager.scrapers._linkedin",
        "_linkedin",
        SocialDataType.POSTS,
        "LinkedIn company updates may be public; personal recent activity normally requires login.",
    ),
    "mastodon": ScraperSpec(
        "mastodon",
        "app.api.social_manager.scrapers._mastodon",
        "_mastodon",
        SocialDataType.POSTS,
    ),
    "pastebin": ScraperSpec(
        "pastebin",
        "app.api.social_manager.scrapers._pastebin",
        "_pastebin",
        SocialDataType.POSTS,
    ),
    "reddit": ScraperSpec(
        "reddit",
        "app.api.social_manager.scrapers._reddit",
        "_reddit",
        SocialDataType.POSTS,
        "The scraper is subreddit/page oriented. The audit defaults Reddit to clearnet via REDDIT_ONION_BASE_URL.",
    ),
    "tiktok": ScraperSpec(
        "tiktok",
        "app.api.social_manager.scrapers._tiktok",
        "_tiktok",
        SocialDataType.POSTS,
        "TikTok content cards are video cards but are requested through the posts data type.",
    ),
    "twitter": ScraperSpec(
        "twitter",
        "app.api.social_manager.scrapers._twitter",
        "_twitter",
        SocialDataType.POSTS,
        "X/Twitter may require a saved session depending on live gating.",
    ),
    "youtube": ScraperSpec(
        "youtube",
        "app.api.social_manager.scrapers._youtube",
        "_youtube",
        SocialDataType.POSTS,
        "YouTube POSTS means community posts, not videos.",
    ),
}


CASES: list[AuditCase] = [
    AuditCase("facebook", "NASA", "https://www.facebook.com/NASA", "page"),
    AuditCase("facebook", "Meta", "https://www.facebook.com/Meta", "page"),
    AuditCase("facebook", "facebook", "https://www.facebook.com/facebook", "page"),
    AuditCase("facebook", "bbcnews", "https://www.facebook.com/bbcnews", "page"),
    AuditCase("facebook", "NPR", "https://www.facebook.com/NPR", "page"),
    AuditCase("facebook", "NatlParkService", "https://www.facebook.com/NatlParkService", "page"),
    AuditCase("facebook", "Olympics", "https://www.facebook.com/olympics", "page"),
    AuditCase("facebook", "CocaCola", "https://www.facebook.com/cocacola", "page"),
    AuditCase("facebook", "Cristiano", "https://www.facebook.com/Cristiano", "public_figure"),
    AuditCase("facebook", "MarkRuffalo", "https://www.facebook.com/MarkRuffalo", "public_figure"),
    AuditCase("instagram", "nasa", "https://www.instagram.com/nasa/", "profile"),
    AuditCase("instagram", "natgeo", "https://www.instagram.com/natgeo/", "profile"),
    AuditCase("instagram", "openai", "https://www.instagram.com/openai/", "profile"),
    AuditCase("instagram", "github", "https://www.instagram.com/github/", "profile"),
    AuditCase("instagram", "nasawebb", "https://www.instagram.com/nasawebb/", "profile"),
    AuditCase("instagram", "theeconomist", "https://www.instagram.com/theeconomist/", "profile"),
    AuditCase("instagram", "wired", "https://www.instagram.com/wired/", "profile"),
    AuditCase("instagram", "lego", "https://www.instagram.com/lego/", "profile"),
    AuditCase("instagram", "nike", "https://www.instagram.com/nike/", "profile"),
    AuditCase("instagram", "airbnb", "https://www.instagram.com/airbnb/", "profile"),
    AuditCase("linkedin", "openai", "https://www.linkedin.com/company/openai/", "company"),
    AuditCase("linkedin", "microsoft", "https://www.linkedin.com/company/microsoft/", "company"),
    AuditCase("linkedin", "google", "https://www.linkedin.com/company/google/", "company"),
    AuditCase("linkedin", "cloudflare", "https://www.linkedin.com/company/cloudflare/", "company"),
    AuditCase("linkedin", "github", "https://www.linkedin.com/company/github/", "company"),
    AuditCase("linkedin", "bkrebs", "https://www.linkedin.com/in/bkrebs/", "profile"),
    AuditCase("linkedin", "reidhoffman", "https://www.linkedin.com/in/reidhoffman/", "profile"),
    AuditCase("linkedin", "jeffweiner08", "https://www.linkedin.com/in/jeffweiner08/", "profile"),
    AuditCase("linkedin", "richardbranson", "https://www.linkedin.com/in/rbranson/", "profile"),
    AuditCase("linkedin", "ariannahuffington", "https://www.linkedin.com/in/ariannahuffington/", "profile"),
    AuditCase("mastodon", "staff", "https://mastodon.social/@staff", "profile"),
    AuditCase("mastodon", "malwaretech", "https://infosec.exchange/@malwaretech", "profile"),
    AuditCase("mastodon", "fosstodon", "https://fosstodon.org/@fosstodon", "profile"),
    AuditCase("mastodon", "opensource", "https://fosstodon.org/@opensource", "profile"),
    AuditCase("mastodon", "Tusky", "https://mastodon.social/@Tusky", "profile"),
    AuditCase("mastodon", "MastodonEngineering", "https://mastodon.social/@MastodonEngineering", "profile"),
    AuditCase("mastodon", "Gargron", "https://mastodon.social/@Gargron", "profile"),
    AuditCase("mastodon", "SwiftOnSecurity", "https://infosec.exchange/@SwiftOnSecurity", "profile"),
    AuditCase("mastodon", "kde", "https://floss.social/@kde", "profile"),
    AuditCase("mastodon", "Vivaldi", "https://social.vivaldi.net/@Vivaldi", "profile"),
    AuditCase("pastebin", "pW3xDnhk", "https://pastebin.com/pW3xDnhk", "paste"),
    AuditCase("pastebin", "CMu7baEY", "https://pastebin.com/CMu7baEY", "paste"),
    AuditCase("pastebin", "jJXaneCA", "https://pastebin.com/jJXaneCA", "paste"),
    AuditCase("pastebin", "wpbdrLbc", "https://pastebin.com/wpbdrLbc", "paste"),
    AuditCase("pastebin", "NQvucZUz", "https://pastebin.com/NQvucZUz", "paste"),
    AuditCase("pastebin", "irwiP55v", "https://pastebin.com/irwiP55v", "paste"),
    AuditCase("pastebin", "FQLLzq35", "https://pastebin.com/FQLLzq35", "paste"),
    AuditCase("pastebin", "wgy29vDW", "https://pastebin.com/wgy29vDW", "paste"),
    AuditCase("pastebin", "JNamyi9N", "https://pastebin.com/JNamyi9N", "paste"),
    AuditCase("pastebin", "prx4G4JD", "https://pastebin.com/prx4G4JD", "paste"),
    AuditCase("reddit", "r/coding", "https://www.reddit.com/r/coding/", "subreddit"),
    AuditCase("reddit", "r/sysadmin", "https://www.reddit.com/r/sysadmin/", "subreddit"),
    AuditCase("reddit", "r/homelab", "https://www.reddit.com/r/homelab/", "subreddit"),
    AuditCase("reddit", "r/learnpython", "https://www.reddit.com/r/learnpython/", "subreddit"),
    AuditCase("reddit", "r/rust", "https://www.reddit.com/r/rust/", "subreddit"),
    AuditCase("reddit", "r/golang", "https://www.reddit.com/r/golang/", "subreddit"),
    AuditCase("reddit", "r/kubernetes", "https://www.reddit.com/r/kubernetes/", "subreddit"),
    AuditCase("reddit", "r/docker", "https://www.reddit.com/r/docker/", "subreddit"),
    AuditCase("reddit", "r/networking", "https://www.reddit.com/r/networking/", "subreddit"),
    AuditCase("reddit", "r/cscareerquestions", "https://www.reddit.com/r/cscareerquestions/", "subreddit"),
    AuditCase("tiktok", "f1", "https://www.tiktok.com/@f1", "profile"),
    AuditCase("tiktok", "nfl", "https://www.tiktok.com/@nfl", "profile"),
    AuditCase("tiktok", "mlb", "https://www.tiktok.com/@mlb", "profile"),
    AuditCase("tiktok", "championsleague", "https://www.tiktok.com/@championsleague", "profile"),
    AuditCase("tiktok", "disney", "https://www.tiktok.com/@disney", "profile"),
    AuditCase("tiktok", "pixar", "https://www.tiktok.com/@pixar", "profile"),
    AuditCase("tiktok", "lego", "https://www.tiktok.com/@lego", "profile"),
    AuditCase("tiktok", "samsung", "https://www.tiktok.com/@samsung", "profile"),
    AuditCase("tiktok", "sony", "https://www.tiktok.com/@sony", "profile"),
    AuditCase("tiktok", "nike", "https://www.tiktok.com/@nike", "profile"),
    AuditCase("twitter", "Apple", "https://x.com/Apple", "profile"),
    AuditCase("twitter", "Amazon", "https://x.com/Amazon", "profile"),
    AuditCase("twitter", "nvidia", "https://x.com/nvidia", "profile"),
    AuditCase("twitter", "Adobe", "https://x.com/Adobe", "profile"),
    AuditCase("twitter", "salesforce", "https://x.com/salesforce", "profile"),
    AuditCase("twitter", "LinkedIn", "https://x.com/LinkedIn", "profile"),
    AuditCase("twitter", "FBI", "https://x.com/FBI", "profile"),
    AuditCase("twitter", "CDCgov", "https://x.com/CDCgov", "profile"),
    AuditCase("twitter", "RedCross", "https://x.com/RedCross", "profile"),
    AuditCase("twitter", "UN", "https://x.com/UN", "profile"),
    AuditCase("youtube", "Microsoft", "https://www.youtube.com/@Microsoft", "channel"),
    AuditCase("youtube", "AdobeCreativeCloud", "https://www.youtube.com/@AdobeCreativeCloud", "channel"),
    AuditCase("youtube", "Netflix", "https://www.youtube.com/@Netflix", "channel"),
    AuditCase("youtube", "Spotify", "https://www.youtube.com/@Spotify", "channel"),
    AuditCase("youtube", "ESPN", "https://www.youtube.com/@ESPN", "channel"),
    AuditCase("youtube", "RedBull", "https://www.youtube.com/@redbull", "channel"),
    AuditCase("youtube", "Veritasium", "https://www.youtube.com/@veritasium", "channel"),
    AuditCase("youtube", "Vox", "https://www.youtube.com/@Vox", "channel"),
    AuditCase("youtube", "CrashCourse", "https://www.youtube.com/@crashcourse", "channel"),
    AuditCase("youtube", "Harvard", "https://www.youtube.com/@harvard", "channel"),
]


class CaseTimeout(RuntimeError):
    pass


def _timeout_handler(signum, frame):
    raise CaseTimeout("case timeout exceeded")


def _safe_error(exc: BaseException) -> str:
    return f"{exc.__class__.__name__}: {exc}"


def _card_content_types(card: Any) -> list[str]:
    return [str(item).strip().lower() for item in (getattr(card, "m_content_type", None) or [])]


def _is_profile_card(card: Any) -> bool:
    content_types = _card_content_types(card)
    return any("profile" in item or "channel_info" in item for item in content_types)


def _is_post_card(card: Any) -> bool:
    content_types = _card_content_types(card)
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


def _sample_card(card: Any) -> dict[str, Any]:
    content = getattr(card, "m_content", None) or ""
    if len(content) > 220:
        content = f"{content[:220]}..."
    return {
        "title": getattr(card, "m_title", None),
        "url": getattr(card, "m_url", None),
        "content_type": list(getattr(card, "m_content_type", None) or []),
        "date": str(getattr(card, "m_date", None) or ""),
        "message_id": getattr(card, "m_message_id", None),
        "content_preview": content,
        "comment_count": getattr(card, "m_comment_count", None),
        "comments_loaded": len(getattr(card, "m_comments", None) or []),
        "profile_image_url": getattr(card, "m_img_src", None),
        "cover_image_url": getattr(card, "m_coverpage", None),
    }


def _first_card_attr(cards: list[Any], attr: str) -> str:
    for card in cards:
        value = getattr(card, attr, None)
        if value:
            return str(value)
    return ""


def _detect_page_state(page: Any) -> dict[str, Any]:
    if page is None:
        return {"state": "unknown", "reason": "page was not created"}
    try:
        current_url = (page.url or "").lower()
    except Exception:
        current_url = ""
    try:
        title = page.title()
    except Exception:
        title = ""
    try:
        body_text = page.locator("body").inner_text(timeout=2500)
    except Exception:
        body_text = ""
    compact_text = " ".join(str(body_text or "").split())
    lower_text = compact_text.lower()

    auth_markers = [
        "authwall",
        "session expired",
        "sign in to continue",
        "log in to continue",
        "sign in to view",
        "log in to see",
        "login to linkedin",
        "sign in to linkedin",
        "sign in to confirm",
        "create new account or log in",
    ]
    rate_markers = [
        "please wait a few minutes",
        "too many requests",
        "rate limit",
        "try again later",
        "temporarily blocked",
    ]
    unavailable_markers = [
        "this content isn't available",
        "content isn't available at the moment",
        "this page isn't available",
        "page not found",
        "profile isn't available",
        "account suspended",
        "doesn't exist",
    ]

    if any(marker in current_url for marker in ["/login", "/checkpoint", "/uas/login", "/accounts/login"]):
        return {"state": "auth_required", "reason": f"redirected to login/checkpoint: {page.url}", "title": title}
    if any(marker in lower_text for marker in rate_markers):
        return {"state": "rate_limited", "reason": compact_text[:220], "title": title}
    if "email or phone" in lower_text and "password" in lower_text and "sign in" in lower_text:
        return {"state": "auth_required", "reason": compact_text[:220], "title": title}
    if any(marker in lower_text for marker in auth_markers):
        return {"state": "auth_required", "reason": compact_text[:220], "title": title}
    if any(marker in lower_text for marker in unavailable_markers):
        return {"state": "unavailable", "reason": compact_text[:220], "title": title}
    return {"state": "loaded", "reason": compact_text[:220], "title": title}


def _empty_status(scraper_status: str, page_state: dict[str, Any], profile_cards: list[Any]) -> str:
    if scraper_status in {
        "auth_required",
        "rate_limited",
        "blocked",
        "http_error",
        "navigation_error",
        "unsupported_data_type",
        "invalid_seed",
        "unavailable",
        "no_public_posts",
    }:
        return scraper_status
    page_status = (page_state or {}).get("state")
    if page_status in {"auth_required", "rate_limited", "unavailable"}:
        return page_status
    if profile_cards:
        return "profile_only"
    return "no_posts"


def _patch_fast_waits(modules: list[Any], wait_ms: int):
    def fast_randint(a, b):
        if b >= 100000:
            return a
        if b >= 1000:
            return wait_ms
        return a

    for module in modules:
        random_module = getattr(module, "random", None)
        if random_module is not None and hasattr(random_module, "randint"):
            random_module.randint = fast_randint


def _reset_scraper(scraper: Any, case: AuditCase, spec: ScraperSpec, item_limit: int, data_type: SocialDataType | None = None):
    scraper._card_data = []
    scraper._entity_data = []
    scraper.callback = None
    scraper.m_seed_url = case.profile_url
    scraper.m_social_data_type = data_type or spec.data_type
    scraper.m_item_limit = item_limit
    scraper.m_comment_limit = 2
    scraper.m_comment_offset = 0
    scraper.m_hash_id = ""
    scraper._last_status = ""
    scraper._last_reason = ""
    if hasattr(scraper, "_helper_methods") and hasattr(scraper._helper_methods, "seen_ids"):
        scraper._helper_methods.seen_ids = set()
    if hasattr(scraper, "_item_list_payloads"):
        scraper._item_list_payloads = []


def _install_route(page, block_resources: set[str]):
    if not block_resources:
        return

    def route_handler(route):
        if route.request.resource_type in block_resources:
            route.abort()
            return
        route.continue_()

    page.route("**/*", route_handler)


def run_case(
    browser,
    case: AuditCase,
    spec: ScraperSpec,
    item_limit: int,
    navigation_timeout_ms: int,
    default_timeout_ms: int,
    case_timeout_s: int,
    block_resources: set[str],
    data_type: SocialDataType | None = None,
) -> CaseResult:
    started = time.monotonic()
    module = importlib.import_module(spec.module_name)
    scraper_cls = getattr(module, spec.class_name)
    scraper = scraper_cls()
    active_data_type = data_type or spec.data_type
    _reset_scraper(scraper, case, spec, item_limit, active_data_type)

    context = None
    page = None
    goto_error = ""
    parse_error = ""
    status = "ok"
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(case_timeout_s)
    try:
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 900},
            locale="en-US",
        )
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        page = context.new_page()
        page.set_default_timeout(default_timeout_ms)
        page.set_default_navigation_timeout(navigation_timeout_ms)
        _install_route(page, block_resources)
        try:
            page.goto(scraper.seed_url, wait_until="domcontentloaded", timeout=navigation_timeout_ms)
        except Exception as exc:
            goto_error = _safe_error(exc)
        try:
            scraper.parse_leak_data(page)
        except Exception as exc:
            parse_error = _safe_error(exc)
            status = "parse_error"
    except CaseTimeout as exc:
        parse_error = _safe_error(exc)
        status = "timeout"
    except Exception as exc:
        parse_error = _safe_error(exc)
        status = "runner_error"
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
        final_url = ""
        page_state: dict[str, Any] = {}
        try:
            final_url = page.url if page is not None else ""
        except Exception:
            final_url = ""
        try:
            page_state = _detect_page_state(page)
        except Exception as exc:
            page_state = {"state": "unknown", "reason": _safe_error(exc)}
        try:
            if context is not None:
                context.close()
        except Exception:
            pass

    cards = list(getattr(scraper, "card_data", None) or [])
    post_cards = [card for card in cards if _is_post_card(card)]
    profile_cards = [card for card in cards if _is_profile_card(card)]
    profile_asset_cards = profile_cards or cards
    profile_image_url = _first_card_attr(profile_asset_cards, "m_img_src")
    cover_image_url = _first_card_attr(profile_asset_cards, "m_coverpage")
    scraper_status = str(getattr(scraper, "_last_status", "") or "")
    scraper_reason = str(getattr(scraper, "_last_reason", "") or "")
    if status == "ok" and active_data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL, SocialDataType.FOLLOWERS, SocialDataType.FOLLOWING):
        if not profile_cards:
            status = _empty_status(scraper_status, page_state, profile_cards)
        elif not profile_image_url and not cover_image_url:
            page_status = (page_state or {}).get("state")
            if scraper_status in {"auth_required", "rate_limited", "blocked", "http_error", "navigation_error", "unavailable"}:
                status = scraper_status
            elif page_status in {"auth_required", "rate_limited", "unavailable"}:
                status = page_status
            else:
                status = "profile_assets_missing"
    elif status == "ok" and not post_cards:
        status = _empty_status(scraper_status, page_state, profile_cards)

    elapsed_ms = int((time.monotonic() - started) * 1000)
    return CaseResult(
        platform=case.platform,
        username=case.username,
        profile_url=case.profile_url,
        kind=case.kind,
        data_type=active_data_type.value,
        status=status,
        returned_posts=bool(post_cards),
        total_cards=len(cards),
        post_cards=len(post_cards),
        profile_cards=len(profile_cards),
        elapsed_ms=elapsed_ms,
        final_url=final_url,
        goto_error=goto_error,
        parse_error=parse_error,
        scraper_status=scraper_status,
        scraper_reason=scraper_reason,
        page_state=page_state,
        has_profile_image=bool(profile_image_url),
        has_cover_image=bool(cover_image_url),
        profile_image_url=profile_image_url,
        cover_image_url=cover_image_url,
        sample_cards=[_sample_card(card) for card in (post_cards or profile_cards)[:2]],
    )


def _selected_cases(platforms: set[str], limit_per_platform: int) -> list[AuditCase]:
    counts: dict[str, int] = {}
    selected: list[AuditCase] = []
    for case in CASES:
        if platforms and case.platform not in platforms:
            continue
        current = counts.get(case.platform, 0)
        if current >= limit_per_platform:
            continue
        selected.append(case)
        counts[case.platform] = current + 1
    return selected


def _summary(results: list[CaseResult]) -> dict[str, Any]:
    platforms = sorted({result.platform for result in results})
    by_platform = {}
    for platform in platforms:
        rows = [result for result in results if result.platform == platform]
        by_platform[platform] = {
            "cases": len(rows),
            "returned_posts_cases": sum(1 for row in rows if row.returned_posts),
            "profile_image_cases": sum(1 for row in rows if row.has_profile_image),
            "cover_image_cases": sum(1 for row in rows if row.has_cover_image),
            "post_cards": sum(row.post_cards for row in rows),
            "profile_cards": sum(row.profile_cards for row in rows),
            "statuses": {
                status: sum(1 for row in rows if row.status == status)
                for status in sorted({row.status for row in rows})
            },
        }
    return {
        "total_cases": len(results),
        "returned_posts_cases": sum(1 for result in results if result.returned_posts),
        "profile_image_cases": sum(1 for result in results if result.has_profile_image),
        "cover_image_cases": sum(1 for result in results if result.has_cover_image),
        "by_platform": by_platform,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", action="append", choices=sorted(SCRAPERS), help="Run only this platform. Can be repeated.")
    parser.add_argument("--data-type", choices=["posts", "profile"], default="posts")
    parser.add_argument("--limit-per-platform", type=int, default=5)
    parser.add_argument("--item-limit", type=int, default=2)
    parser.add_argument("--case-timeout", type=int, default=45, help="Seconds before one case is marked timeout.")
    parser.add_argument("--navigation-timeout-ms", type=int, default=20000)
    parser.add_argument("--default-timeout-ms", type=int, default=10000)
    parser.add_argument("--fast-wait-ms", type=int, default=750)
    parser.add_argument("--output", default="", help="JSON report path. Defaults to /tmp/social_scraper_live_audit_<timestamp>.json.")
    parser.add_argument("--keep-media", action="store_true", help="Do not block image/media/font resources.")
    parser.add_argument("--reddit-onion", action="store_true", help="Use the scraper's default Reddit onion URL instead of clearnet.")
    parser.add_argument("--isolate-cases", action="store_true", help="Run each case in a killable subprocess.")
    parser.add_argument("--worker-case", type=int, default=None, help=argparse.SUPPRESS)
    return parser.parse_args()


def _base_report(args: argparse.Namespace, selected_cases: list[AuditCase], timestamp: str) -> dict[str, Any]:
    block_resources = set() if args.keep_media else {"image", "media", "font"}
    return {
        "generated_at": timestamp,
        "repo_root": str(REPO_ROOT),
        "settings": {
            "limit_per_platform": args.limit_per_platform,
            "item_limit": args.item_limit,
            "case_timeout": args.case_timeout,
            "navigation_timeout_ms": args.navigation_timeout_ms,
            "default_timeout_ms": args.default_timeout_ms,
            "fast_wait_ms": args.fast_wait_ms,
            "block_resources": sorted(block_resources),
            "reddit_base": os.getenv("REDDIT_ONION_BASE_URL", ""),
            "isolate_cases": bool(args.isolate_cases),
            "data_type": args.data_type,
        },
        "scrapers": {platform: asdict(spec) | {"data_type": spec.data_type.value} for platform, spec in SCRAPERS.items()},
        "cases": [asdict(case) for case in selected_cases],
        "results": [],
        "summary": {},
    }


def _write_report(output_path: Path, report: dict[str, Any], results: list[CaseResult]):
    report["results"] = [asdict(result) for result in results]
    report["summary"] = _summary(results)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"report={output_path}", flush=True)
    print(json.dumps(report["summary"], indent=2, sort_keys=True), flush=True)


def _run_in_process(args: argparse.Namespace, selected_cases: list[AuditCase], output_path: Path, report: dict[str, Any]) -> int:
    modules = [importlib.import_module(spec.module_name) for spec in SCRAPERS.values()]
    _patch_fast_waits(modules, args.fast_wait_ms)
    block_resources = set() if args.keep_media else {"image", "media", "font"}
    active_data_type = SocialDataType.PROFILE if args.data_type == "profile" else None
    results: list[CaseResult] = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                ],
            )
            try:
                for index, case in enumerate(selected_cases, start=1):
                    spec = SCRAPERS[case.platform]
                    print(
                        f"[{index:02d}/{len(selected_cases):02d}] {case.platform:<9} "
                        f"{case.username:<22} {case.profile_url}",
                        flush=True,
                    )
                    try:
                        result = run_case(
                            browser=browser,
                            case=case,
                            spec=spec,
                            item_limit=args.item_limit,
                            navigation_timeout_ms=args.navigation_timeout_ms,
                            default_timeout_ms=args.default_timeout_ms,
                            case_timeout_s=args.case_timeout,
                            block_resources=block_resources,
                            data_type=active_data_type,
                        )
                    except Exception as exc:
                        result = CaseResult(
                            platform=case.platform,
                            username=case.username,
                            profile_url=case.profile_url,
                            kind=case.kind,
                            data_type=spec.data_type.value,
                            status="runner_error",
                            returned_posts=False,
                            total_cards=0,
                            post_cards=0,
                            profile_cards=0,
                            elapsed_ms=0,
                            parse_error=f"{_safe_error(exc)}\n{traceback.format_exc()}",
                            sample_cards=[],
                        )
                    results.append(result)
                    print(
                        f"    status={result.status} returned_posts={result.returned_posts} "
                        f"cards={result.total_cards} post_cards={result.post_cards} "
                        f"profile_img={result.has_profile_image} cover_img={result.has_cover_image} "
                        f"elapsed_ms={result.elapsed_ms}",
                        flush=True,
                    )
            finally:
                browser.close()
    finally:
        _write_report(output_path, report, results)

    return 0


def _timeout_result(case: AuditCase, spec: ScraperSpec, timeout_s: int, stdout: str) -> CaseResult:
    tail = "\n".join((stdout or "").splitlines()[-20:])
    return CaseResult(
        platform=case.platform,
        username=case.username,
        profile_url=case.profile_url,
        kind=case.kind,
        data_type=spec.data_type.value,
        status="timeout",
        returned_posts=False,
        total_cards=0,
        post_cards=0,
        profile_cards=0,
        elapsed_ms=timeout_s * 1000,
        parse_error=f"worker exceeded {timeout_s}s timeout\n{tail}",
        sample_cards=[],
    )


def _worker_error_result(case: AuditCase, spec: ScraperSpec, elapsed_ms: int, message: str) -> CaseResult:
    return CaseResult(
        platform=case.platform,
        username=case.username,
        profile_url=case.profile_url,
        kind=case.kind,
        data_type=spec.data_type.value,
        status="runner_error",
        returned_posts=False,
        total_cards=0,
        post_cards=0,
        profile_cards=0,
        elapsed_ms=elapsed_ms,
        parse_error=message,
        sample_cards=[],
    )


def _read_worker_result(case_output: Path, case: AuditCase, spec: ScraperSpec, elapsed_ms: int, stdout: str, returncode: int) -> CaseResult:
    if not case_output.exists():
        return _worker_error_result(
            case,
            spec,
            elapsed_ms,
            f"worker exited {returncode} without report\n{stdout[-4000:]}",
        )
    try:
        report = json.loads(case_output.read_text(encoding="utf-8"))
        rows = report.get("results") or []
        if not rows:
            return _worker_error_result(
                case,
                spec,
                elapsed_ms,
                f"worker report had no result rows; returncode={returncode}\n{stdout[-4000:]}",
            )
        row = rows[0]
        result = CaseResult(**row)
        if returncode != 0 and result.status == "ok":
            result.status = "runner_error"
            result.parse_error = f"worker exited {returncode}\n{stdout[-4000:]}"
        return result
    except Exception as exc:
        return _worker_error_result(
            case,
            spec,
            elapsed_ms,
            f"failed to read worker report: {_safe_error(exc)}\n{stdout[-4000:]}",
        )


def _run_isolated(args: argparse.Namespace, selected_cases: list[AuditCase], output_path: Path, report: dict[str, Any], timestamp: str) -> int:
    results: list[CaseResult] = []
    worker_timeout = args.case_timeout + 20
    script_path = Path(__file__).resolve()
    for index, case in enumerate(selected_cases, start=1):
        spec = SCRAPERS[case.platform]
        global_index = CASES.index(case)
        case_output = Path("/tmp") / f"social_scraper_live_audit_case_{timestamp}_{global_index}.json"
        if case_output.exists():
            try:
                case_output.unlink()
            except Exception:
                pass
        command = [
            sys.executable,
            str(script_path),
            "--worker-case",
            str(global_index),
            "--data-type",
            args.data_type,
            "--item-limit",
            str(args.item_limit),
            "--case-timeout",
            str(args.case_timeout),
            "--navigation-timeout-ms",
            str(args.navigation_timeout_ms),
            "--default-timeout-ms",
            str(args.default_timeout_ms),
            "--fast-wait-ms",
            str(args.fast_wait_ms),
            "--output",
            str(case_output),
        ]
        if args.keep_media:
            command.append("--keep-media")
        if args.reddit_onion:
            command.append("--reddit-onion")
        print(
            f"[{index:02d}/{len(selected_cases):02d}] {case.platform:<9} "
            f"{case.username:<22} {case.profile_url}",
            flush=True,
        )
        started = time.monotonic()
        env = os.environ.copy()
        if not args.reddit_onion:
            env.setdefault("REDDIT_ONION_BASE_URL", "https://www.reddit.com")
        process = subprocess.Popen(
            command,
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
            env=env,
        )
        stdout = ""
        try:
            stdout, _ = process.communicate(timeout=worker_timeout)
            elapsed_ms = int((time.monotonic() - started) * 1000)
            result = _read_worker_result(case_output, case, spec, elapsed_ms, stdout, process.returncode)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except Exception:
                process.kill()
            try:
                stdout, _ = process.communicate(timeout=5)
            except Exception:
                stdout = stdout or ""
            result = _timeout_result(case, spec, worker_timeout, stdout)
        results.append(result)
        print(
            f"    status={result.status} returned_posts={result.returned_posts} "
            f"cards={result.total_cards} post_cards={result.post_cards} "
            f"profile_img={result.has_profile_image} cover_img={result.has_cover_image} "
            f"elapsed_ms={result.elapsed_ms}",
            flush=True,
        )
        report["results"] = [asdict(row) for row in results]
        report["summary"] = _summary(results)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(output_path, report, results)
    return 0


def main() -> int:
    args = parse_args()
    if not args.reddit_onion:
        os.environ.setdefault("REDDIT_ONION_BASE_URL", "https://www.reddit.com")

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_path = Path(args.output) if args.output else Path("/tmp") / f"social_scraper_live_audit_{timestamp}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.worker_case is not None:
        selected_cases = [CASES[args.worker_case]]
        report = _base_report(args, selected_cases, timestamp)
        return _run_in_process(args, selected_cases, output_path, report)

    platforms = set(args.platform or [])
    selected_cases = _selected_cases(platforms, args.limit_per_platform)
    report = _base_report(args, selected_cases, timestamp)
    if args.isolate_cases:
        return _run_isolated(args, selected_cases, output_path, report, timestamp)
    return _run_in_process(args, selected_cases, output_path, report)


if __name__ == "__main__":
    raise SystemExit(main())
