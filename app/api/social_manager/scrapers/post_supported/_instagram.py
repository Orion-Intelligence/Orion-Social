import re
import random
from abc import ABC
from typing import List, Callable, Optional
from datetime import datetime
import gzip
import json
import os
import socket
from urllib import parse as urlparse
from urllib import error as urlerror
from urllib import request as urlrequest

import requests
from playwright.sync_api import Page

from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model, social_comment_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method

class _instagram(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.platform = "instagram"
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self._initialized = None
        self.m_seed_url = ""
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._last_status = ""
        self._last_reason = ""

    def init_callback(self, callback=None):
        self.callback = callback

    @property
    def is_crawled(self) -> bool:
        return self._is_crawled

    @property
    def seed_url(self) -> str:
        return self.m_seed_url

    @property
    def developer_signature(self) -> str:
        return "Muhammad Hannan Zahid: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hOii"

    @property
    def base_url(self) -> str:
        return "https://www.instagram.com/"

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def invoke_db(self, command: int, key: str, default_value, expiry: int | None = None):
        return self._redis_instance.invoke_trigger(command, [key + self.__class__.__name__, default_value, expiry])

    def contact_page(self) -> str:
        return self.seed_url

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.TOR,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_threat_type=ThreatType.INSTAGRAM,
            m_rule_type=RuleType.INSTAGRAM,
            m_social_data_type=getattr(self, "m_social_data_type", SocialDataType.DEFAULT),
            m_resoource_block=False,
        )

    def _apply_saved_session(self, page) -> bool:
        context_id = id(page.context)
        if getattr(self, "_instagram_session_context_id", None) == context_id:
            return True

        sessions_dir = os.getenv("ORION_SESSION_ROOT") or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sessions")
        session_paths = [
            os.path.join(sessions_dir, "instagramscraper_session.json.gz"),
            os.path.join(sessions_dir, "_instagram_session.json.gz"),
        ]
        for session_path in session_paths:
            if not os.path.exists(session_path):
                continue
            try:
                with gzip.open(session_path, "rt", encoding="utf-8") as f:
                    state = json.load(f)
                cookies = state.get("cookies") or []
                if cookies:
                    page.context.add_cookies(cookies)
                try:
                    for key, value in (state.get("local_storage") or {}).items():
                        page.evaluate("([key, value]) => window.localStorage.setItem(key, value)", [key, value])
                    for key, value in (state.get("session_storage") or {}).items():
                        page.evaluate("([key, value]) => window.sessionStorage.setItem(key, value)", [key, value])
                except Exception:
                    pass
                self._instagram_session_context_id = context_id
                return True
            except Exception:
                continue
        self._instagram_session_context_id = context_id
        return False

    @staticmethod
    def _is_wrong_profile_page(page: Page, target_username: str) -> bool:
        try:
            current_url = (page.url or "").lower()
            if f"/{target_username.lower()}" in current_url:
                return False
            if "/accounts/login/" in current_url and f"%2f{target_username.lower()}%2f" in current_url:
                return False
            body_text = page.locator("body").inner_text(timeout=3000)
            return bool(
                "Use another profile" in body_text
                or "Continue" in body_text and "Create new account" in body_text
                or current_url.rstrip("/") == "https://www.instagram.com"
            )
        except Exception:
            return False

    @staticmethod
    def _clear_browser_session(page: Page):
        try:
            page.context.clear_cookies()
        except Exception:
            pass
        try:
            page.evaluate("""() => {
                try { window.localStorage.clear(); } catch (_) {}
                try { window.sessionStorage.clear(); } catch (_) {}
            }""")
        except Exception:
            pass

    def _item_limit(self) -> int:
        try:
            return max(1, min(int(getattr(self, "m_item_limit", 10) or 10), 100))
        except Exception:
            return 10

    def _set_fetch_status(self, status_code: int | None, payload: dict | None = None, fallback: str = ""):
        payload = payload or {}
        message = helper_method.scalar_text(payload.get("message")) or fallback
        status_text = helper_method.scalar_text(payload.get("status"))
        if status_code in (401, 403) or payload.get("require_login"):
            self._last_status = "auth_required"
            self._last_reason = message or "instagram web profile endpoint requires login"
        elif status_code == 429 or "try again" in message.lower() or "wait a few minutes" in message.lower():
            self._last_status = "rate_limited"
            self._last_reason = message or "instagram web profile endpoint is rate limited"
        elif status_code and status_code >= 400:
            self._last_status = "http_error"
            self._last_reason = f"instagram web profile endpoint returned HTTP {status_code}"
        elif status_text == "fail" and message:
            self._last_status = "blocked"
            self._last_reason = message

    @staticmethod
    def _tor_proxy_candidates() -> list[str]:
        candidates = [
            os.getenv("INSTAGRAM_TOR_PROXY_URL"),
            os.getenv("TOR_PROXY_URL"),
            "socks5h://trusted-social_tor_instace_1:9552",
            "socks5h://172.25.0.10:9552",
            "socks5h://127.0.0.1:9050",
            "socks5h://127.0.0.1:9150",
        ]
        cleaned = []
        for candidate in candidates:
            value = helper_method.scalar_text(candidate)
            if value and value not in cleaned:
                cleaned.append(value)
        return cleaned

    def _fetch_web_profile_info_via_tor(self, endpoint: str, headers: dict, original_status: str, original_reason: str) -> dict:
        if str(os.getenv("INSTAGRAM_DISABLE_TOR_FALLBACK", "")).strip().lower() in {"1", "true", "yes"}:
            return {}

        try:
            timeout = max(2.0, min(float(os.getenv("INSTAGRAM_TOR_TIMEOUT_SEC", "5") or 5), 12.0))
        except Exception:
            timeout = 5.0
        try:
            max_attempts = max(1, min(int(os.getenv("INSTAGRAM_TOR_MAX_ATTEMPTS", "6") or 6), 6))
        except Exception:
            max_attempts = 6

        for proxy_url in self._tor_proxy_candidates()[:max_attempts]:
            proxies = {"http": proxy_url, "https": proxy_url}
            previous_socket_timeout = socket.getdefaulttimeout()
            try:
                socket.setdefaulttimeout(timeout)
                response = requests.get(endpoint, headers=headers, proxies=proxies, timeout=(timeout, timeout))
                payload = response.json() if response.content else {}
                user_data = (payload.get("data") or {}).get("user") if isinstance(payload, dict) else {}
                if response.ok and user_data:
                    self._last_status = "ok"
                    self._last_reason = f"instagram Tor fallback returned user data via {proxy_url}"
                    return user_data
                self._set_fetch_status(response.status_code, payload if isinstance(payload, dict) else {})
            except Exception:
                continue
            finally:
                socket.setdefaulttimeout(previous_socket_timeout)

        self._last_status = original_status
        self._last_reason = original_reason
        return {}

    def _comment_limit(self) -> int:
        try:
            return max(1, min(int(getattr(self, "m_comment_limit", 10) or 10), 10))
        except Exception:
            return 10

    def _comment_offset(self) -> int:
        try:
            return max(0, int(getattr(self, "m_comment_offset", 0) or 0))
        except Exception:
            return 0

    @staticmethod
    def _is_profile_data_type(data_type: SocialDataType) -> bool:
        return data_type in (
            SocialDataType.PROFILE,
            SocialDataType.CHANNEL,
        )

    @staticmethod
    def _extract_profile_assets(page: Page) -> dict:
        try:
            return page.evaluate("""() => {
                const cleanUrl = value => {
                    if (!value) return '';
                    const raw = String(value);
                    if (!raw || raw.startsWith('data:') || /^(none|initial|inherit|unset)$/i.test(raw.trim())) return '';
                    try { return new URL(raw, location.href).href; } catch (_) { return raw; }
                };
                const firstAttr = (selectors, attr) => {
                    for (const selector of selectors) {
                        const node = document.querySelector(selector);
                        const value = node?.getAttribute(attr) || node?.[attr] || '';
                        const url = cleanUrl(value);
                        if (url) return url;
                    }
                    return '';
                };
                const profileIcon = firstAttr([
                    'meta[property="og:image"]',
                    'meta[name="twitter:image"]',
                    'header img[alt*="profile picture" i]',
                    'header img'
                ], 'content') || firstAttr([
                    'header img[alt*="profile picture" i]',
                    'header img'
                ], 'src');
                return {profileIcon, coverpage: ''};
            }""") or {}
        except Exception:
            return {}

    @staticmethod
    def _dismiss_login_modal(page: Page):
        try:
            page.evaluate("""() => {
                const modalText = dialog => String(dialog.innerText || dialog.textContent || '');
                for (const dialog of document.querySelectorAll('div[role="dialog"]')) {
                    if (dialog.querySelector('article')) continue;
                    const text = modalText(dialog);
                    const isLoginWall = /See photos, videos and more from|Sign up and never miss a post|By continuing, you agree to Instagram/i.test(text);
                    if (!isLoginWall) continue;
                    const closeButton = dialog.querySelector('svg[aria-label="Close"]')?.closest('[role="button"], button');
                    if (closeButton) {
                        try { closeButton.click(); } catch (_) {}
                    }
                }
            }""")
            page.wait_for_timeout(500)
        except Exception:
            pass

        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
        except Exception:
            pass

        try:
            page.evaluate("""() => {
                for (const dialog of document.querySelectorAll('div[role="dialog"]')) {
                    if (dialog.querySelector('article')) continue;
                    const text = String(dialog.innerText || dialog.textContent || '');
                    const isLoginWall = /See photos, videos and more from|Sign up and never miss a post|By continuing, you agree to Instagram/i.test(text);
                    if (!isLoginWall) continue;
                    const shell = dialog.closest('[aria-modal="true"]') || dialog.parentElement || dialog;
                    shell.remove();
                }
            }""")
        except Exception:
            pass

    def _extract_grid_items_from_page(
        self,
        page: Page,
        target_username: str,
        content_type: str,
        limit: int,
        max_comments: int,
        comment_offset: int,
        on_item: Optional[Callable[[dict], None]] = None,
    ) -> list:
        rows = []
        for _ in range(20):
            try:
                rows = page.evaluate("""(limit) => {
                    const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                    const srcsetUrl = value => String(value || '').split(',').pop().trim().split(/\\s+/)[0] || '';
                    const anchors = Array.from(document.querySelectorAll('main a[href*="/p/"], main a[href*="/reel/"]'));
                    const seen = new Set();
                    const rows = [];
                    for (const anchor of anchors) {
                        const href = anchor.href || anchor.getAttribute('href') || '';
                        if (!href || seen.has(href)) continue;
                        seen.add(href);
                        const img = anchor.querySelector('img');
                        const media = img?.currentSrc || img?.src || img?.getAttribute('src') || srcsetUrl(img?.getAttribute('srcset')) || '';
                        const caption = clean(img?.alt || anchor.getAttribute('aria-label') || anchor.innerText || '');
                        const match = href.match(/\\/(p|reel)\\/([^/?#]+)/);
                        rows.push({
                            type: match?.[1] === 'reel' ? 'reel' : 'post',
                            post_url: href,
                            post_id: match?.[2] || href.split('/').filter(Boolean).pop() || '',
                            caption,
                            media,
                        });
                        if (rows.length >= limit) break;
                    }
                    return rows;
                }""", max(1, min(int(limit or 10), 100))) or []
            except Exception:
                rows = []
            if len(rows) >= max(1, min(int(limit or 10), 100)):
                break
            try:
                previous_height = page.evaluate("document.body ? document.body.scrollHeight : 0")
                page.mouse.wheel(0, random.randint(1800, 3200))
                page.wait_for_timeout(random.randint(900, 1800))
                new_height = page.evaluate("document.body ? document.body.scrollHeight : 0")
                if len(rows) > 0 and new_height == previous_height:
                    break
            except Exception:
                break
        if not rows and target_username:
            rows = self._extract_grid_items_from_web_profile(page, target_username, limit, allow_tor=False)

        extracted_data = []
        comment_target_count = max(0, comment_offset) + max(0, max_comments)
        for row in rows:
            item = {
                "type": helper_method.scalar_text(row.get("type")) or content_type,
                "time": helper_method.scalar_text(row.get("time")) or None,
                "likes": row.get("likes", 0),
                "caption": helper_method.scalar_text(row.get("caption")),
                "comments": [],
                "comment_count": helper_method.scalar_text(row.get("comment_count")),
                "post_url": helper_method.scalar_text(row.get("post_url")),
                "post_id": helper_method.scalar_text(row.get("post_id")),
                "media": helper_method.scalar_text(row.get("media")),
            }
            if comment_target_count:
                item["comments"] = []
            extracted_data.append(item)
            if on_item:
                on_item(item)
        return extracted_data

    def _fetch_web_profile_info(self, page: Page | None, target_username: str, allow_tor: bool = True) -> dict:
        endpoint = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={urlparse.quote(target_username)}"
        headers = {
            "x-ig-app-id": "936619743392459",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            "accept": "application/json,text/plain,*/*",
        }
        direct_attempted = True
        try:
            req = urlrequest.Request(endpoint, headers=headers)
            with urlrequest.urlopen(req, timeout=8) as response:
                payload = json.loads(response.read().decode("utf-8", errors="replace") or "{}")
            user_data = (payload.get("data") or {}).get("user") or {}
            if user_data:
                self._last_status = "ok"
                self._last_reason = "instagram urllib request returned user data"
                return user_data
        except urlerror.HTTPError as exc:
            payload = {}
            try:
                payload = json.loads(exc.read().decode("utf-8", errors="replace") or "{}")
            except Exception:
                pass
            self._set_fetch_status(exc.code, payload)
        except Exception:
            pass

        if allow_tor and self._last_status in {"auth_required", "rate_limited", "blocked", "http_error"}:
            original_status = self._last_status
            original_reason = self._last_reason
            tor_user_data = self._fetch_web_profile_info_via_tor(endpoint, headers, original_status, original_reason)
            if tor_user_data:
                return tor_user_data

        if page is not None:
            try:
                raw = page.evaluate(
                    """async ([endpoint, headers, timeoutMs]) => {
                        const controller = new AbortController();
                        const timer = setTimeout(() => controller.abort(), timeoutMs);
                        try {
                            const response = await fetch(endpoint, {credentials: 'include', headers, signal: controller.signal});
                            return {status: response.status, ok: response.ok, text: await response.text()};
                        } catch (error) {
                            return {status: 0, ok: false, text: '', error: String(error && error.message || error)};
                        } finally {
                            clearTimeout(timer);
                        }
                    }""",
                    [endpoint, headers, 8000],
                ) or {}
                raw_text = raw.get("text") if isinstance(raw, dict) else raw
                payload = json.loads(raw_text or "{}")
                user_data = (payload.get("data") or {}).get("user") or {}
                if user_data:
                    self._last_status = "ok"
                    self._last_reason = "instagram web profile endpoint returned user data"
                    return user_data
                if isinstance(raw, dict):
                    self._set_fetch_status(raw.get("status"), payload, raw.get("error") or "")
            except Exception:
                pass
            try:
                response = page.context.request.get(endpoint, headers=headers, timeout=20000)
                if response.ok:
                    payload = response.json()
                    user_data = (payload.get("data") or {}).get("user") or {}
                    if user_data:
                        self._last_status = "ok"
                        self._last_reason = "instagram context request returned user data"
                        return user_data
                else:
                    payload = {}
                    try:
                        payload = response.json()
                    except Exception:
                        pass
                    self._set_fetch_status(response.status, payload)
            except Exception:
                pass

        if allow_tor and self._last_status in {"auth_required", "rate_limited", "blocked", "http_error"}:
            original_status = self._last_status
            original_reason = self._last_reason
            tor_user_data = self._fetch_web_profile_info_via_tor(endpoint, headers, original_status, original_reason)
            if tor_user_data:
                return tor_user_data

        if not direct_attempted:
            try:
                req = urlrequest.Request(endpoint, headers=headers)
                with urlrequest.urlopen(req, timeout=8) as response:
                    payload = json.loads(response.read().decode("utf-8", errors="replace") or "{}")
                user_data = (payload.get("data") or {}).get("user") or {}
                if user_data:
                    self._last_status = "ok"
                    self._last_reason = "instagram urllib request returned user data"
                return user_data
            except urlerror.HTTPError as exc:
                payload = {}
                try:
                    payload = json.loads(exc.read().decode("utf-8", errors="replace") or "{}")
                except Exception:
                    pass
                self._set_fetch_status(exc.code, payload)
            except Exception:
                pass
        original_status = self._last_status
        original_reason = self._last_reason
        if allow_tor:
            tor_user_data = self._fetch_web_profile_info_via_tor(endpoint, headers, original_status, original_reason)
            if tor_user_data:
                return tor_user_data
        return {}

    def _extract_grid_items_from_web_profile(self, page: Page | None, target_username: str, limit: int, user_data: dict | None = None, allow_tor: bool = True) -> list[dict]:
        user_data = user_data or self._fetch_web_profile_info(page, target_username, allow_tor=allow_tor)
        media_sections = [
            user_data.get("edge_owner_to_timeline_media") or {},
            user_data.get("edge_felix_video_timeline") or {},
        ]
        edges = []
        seen_shortcodes = set()
        for media in media_sections:
            for edge in media.get("edges") or []:
                node = edge.get("node") if isinstance(edge, dict) else {}
                shortcode = helper_method.scalar_text(node.get("shortcode")) if isinstance(node, dict) else ""
                if not shortcode or shortcode in seen_shortcodes:
                    continue
                seen_shortcodes.add(shortcode)
                edges.append(edge)
        rows = []
        for edge in edges[:max(1, min(int(limit or 10), 100))]:
            node = edge.get("node") if isinstance(edge, dict) else {}
            if not isinstance(node, dict):
                continue
            shortcode = helper_method.scalar_text(node.get("shortcode"))
            if not shortcode:
                continue
            caption_edges = ((node.get("edge_media_to_caption") or {}).get("edges") or [])
            caption = ""
            if caption_edges:
                caption = helper_method.scalar_text(((caption_edges[0] or {}).get("node") or {}).get("text"))
            timestamp = None
            try:
                raw_timestamp = int(node.get("taken_at_timestamp") or 0)
                if raw_timestamp:
                    timestamp = datetime.fromtimestamp(raw_timestamp).isoformat()
            except Exception:
                timestamp = None
            is_reel = bool(node.get("is_video")) and node.get("__typename") == "GraphVideo"
            rows.append({
                "type": "reel" if is_reel else "post",
                "time": timestamp,
                "likes": (node.get("edge_liked_by") or node.get("edge_media_preview_like") or {}).get("count") or 0,
                "caption": caption,
                "comments": [],
                "comment_count": (node.get("edge_media_to_comment") or {}).get("count"),
                "post_url": f"https://www.instagram.com/{'reel' if is_reel else 'p'}/{shortcode}/",
                "post_id": shortcode,
                "media": node.get("display_url") or node.get("thumbnail_src") or "",
            })
        return rows

    @staticmethod
    def _profile_info_from_web_profile(user_data: dict, target_username: str, fallback_assets: dict | None = None) -> dict:
        fallback_assets = fallback_assets or {}
        if not isinstance(user_data, dict):
            user_data = {}
        media = user_data.get("edge_owner_to_timeline_media") or {}
        video_media = user_data.get("edge_felix_video_timeline") or {}
        posts = media.get("count")
        if posts is None:
            posts = video_media.get("count")
        parts = []
        if posts is not None:
            parts.append(f"POSTS: {posts}")
        return {
            "username": helper_method.scalar_text(user_data.get("username")) or target_username,
            "real_name": helper_method.scalar_text(user_data.get("full_name")),
            "bio": helper_method.scalar_text(user_data.get("biography")),
            "group_info": " | ".join(parts),
            "profileIcon": helper_method.scalar_text(user_data.get("profile_pic_url_hd") or user_data.get("profile_pic_url")) or fallback_assets.get("profileIcon"),
            "coverpage": fallback_assets.get("coverpage"),
        }


    def parse_ig_count(self, text: str) -> int:
        if not text:
            return 0
        match = re.search(r"([\d\.,]+)\s*([KkMm]?)", text)

        if not match:
            return 0
        num_str = match.group(1).replace(",", "")
        suffix = match.group(2).upper()

        try:
            val = float(num_str)

            if suffix == "K":
                val *= 1000
            elif suffix == "M":
                val *= 1000000
            return int(val)
        except Exception:
            return 0

    def extract_grid_items(
        self,
        page: Page,
        target_username: str,
        content_selector: str,
        content_type: str,
        limit: int = 10,
        max_comments: int = 10,
        comment_offset: int = 0,
        on_item: Optional[Callable[[dict], None]] = None
    ) -> list:
        _ = target_username
        extracted_data = []
        try:
            self._dismiss_login_modal(page)
            page.wait_for_selector(content_selector, timeout=10000)
            self._dismiss_login_modal(page)
            page.wait_for_timeout(random.randint(1000, 10000))
        except Exception:
            return self._extract_grid_items_from_page(page, target_username, content_type, limit, max_comments, comment_offset, on_item)

        if page.locator(content_selector).count() == 0:
            return self._extract_grid_items_from_page(page, target_username, content_type, limit, max_comments, comment_offset, on_item)

        if max_comments <= 0:
            return self._extract_grid_items_from_page(page, target_username, content_type, limit, max_comments, comment_offset, on_item)

        try:
            page.locator(content_selector).first.click()
            page.wait_for_timeout(1000)
            self._dismiss_login_modal(page)
            page.wait_for_selector("div[role='dialog'] article", timeout=10000)
            page.wait_for_timeout(random.randint(1000, 10000))
        except Exception:
            self._dismiss_login_modal(page)
            return self._extract_grid_items_from_page(page, target_username, content_type, limit, max_comments, comment_offset, on_item)

        for _ in range(limit):
            dialog = page.locator("div[role='dialog']")
            if dialog.count() == 0 or dialog.locator("article").count() == 0:
                self._dismiss_login_modal(page)
                if not extracted_data:
                    return self._extract_grid_items_from_page(page, target_username, content_type, limit, max_comments, comment_offset, on_item)
                break

            try:
                dialog.locator("time").first.wait_for(timeout=5000)
            except Exception:
                pass

            post_url = ""
            post_id = ""
            try:
                link_loc = dialog.locator("a[href*='/p/'], a[href*='/reel/']").first
                if link_loc.count() > 0:
                    post_url = link_loc.get_attribute("href") or ""
                    if post_url.startswith("/"):
                        post_url = f"https://www.instagram.com{post_url}"
                    parts = [p for p in post_url.split("/") if p]
                    if parts:
                        post_id = parts[-1]
            except Exception:
                pass

            post_time_loc = dialog.locator("time").first
            post_time = post_time_loc.get_attribute("datetime") if post_time_loc.count() > 0 else None

            likes_loc = dialog.locator("section.x12nagc, section.x182iqb8").filter(has_text="likes").first
            raw_likes = likes_loc.inner_text() if likes_loc.count() > 0 else ""
            post_likes = self.parse_ig_count(raw_likes or "")

            caption_loc = dialog.locator("h1[dir='auto']").filter(visible=True).first
            if caption_loc.count() > 0:
                post_caption = caption_loc.inner_text() or ""
            else:
                fallback_caption_loc = dialog.locator("div._a9zs span")
                raw_post_caption = fallback_caption_loc.first.inner_text() if fallback_caption_loc.count() > 0 else ""
                post_caption = raw_post_caption or ""

            extracted_comments = []
            previous_comment_count = -1
            comment_target_count = max(0, comment_offset) + max(0, max_comments)
            while len(extracted_comments) < comment_target_count:
                comment_nodes = dialog.locator("li._a9zj, li._a9zl").all()
                for node in comment_nodes:
                    try:
                        c_user_loc = node.locator("h3").first
                        if c_user_loc.count() == 0:
                            continue
                        raw_c_user = c_user_loc.inner_text()
                        c_user = raw_c_user.strip() if raw_c_user else ""
                        c_text_loc = node.locator("span._ap3a._aaco._aacu._aacx._aad7._aade").filter(visible=True).first
                        raw_c_text = c_text_loc.inner_text() if c_text_loc.count() > 0 else ""
                        c_text = raw_c_text.strip() if raw_c_text else ""
                        if not c_text:
                            continue
                        comment_obj = {"username": c_user, "text": c_text}
                        if comment_obj not in extracted_comments:
                            extracted_comments.append(comment_obj)
                        if len(extracted_comments) >= comment_target_count:
                            break
                    except Exception:
                        continue

                if len(extracted_comments) == previous_comment_count:
                    break
                previous_comment_count = len(extracted_comments)
                load_more_btn = dialog.locator("button:has(svg[aria-label='Load more comments'])").first
                if load_more_btn.count() > 0 and load_more_btn.is_visible():
                    try:
                        load_more_btn.click()
                        page.wait_for_timeout(random.randint(1000, 10000))
                    except Exception:
                        break
                else:
                    break

            if post_time or post_caption or post_likes > 0:
                item = {
                    "type": content_type,
                    "time": post_time,
                    "likes": post_likes,
                    "caption": post_caption,
                    "comments": extracted_comments[comment_offset:comment_target_count] if comment_target_count else [],
                    "post_url": post_url,
                    "post_id": post_id
                }
                extracted_data.append(item)
                if on_item:
                    on_item(item)

            next_btn = dialog.locator("button:has(svg[aria-label='Next'])").first
            if next_btn.count() > 0 and next_btn.is_visible():
                try:
                    next_btn.click()
                    page.wait_for_timeout(random.randint(1000, 10000))
                except Exception:
                    break
            else:
                break

        page.keyboard.press("Escape")
        page.wait_for_timeout(random.randint(1000, 10000))
        if not extracted_data:
            return self._extract_grid_items_from_page(page, target_username, content_type, limit, max_comments, comment_offset, on_item)
        return extracted_data

    def parse_leak_data(self, page: Page):
        self._card_data = []
        self._entity_data = []
        self._last_status = ""
        self._last_reason = ""
        target_url = self.m_seed_url
        target_username = target_url.rstrip("/").split("/")[-1]
        data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
        posts_limit = self._item_limit()
        comments_per_post = self._comment_limit() if data_type == SocialDataType.COMMENTS else 0
        is_profile_request = self._is_profile_data_type(data_type)
        self._apply_saved_session(page)
        web_profile_data = {} if is_profile_request else self._fetch_web_profile_info(page, target_username, allow_tor=False)

        if is_profile_request and web_profile_data:
            profile_info = self._profile_info_from_web_profile(web_profile_data, target_username, {})
            card_data = social_model(
                m_title=profile_info.get("username") or target_username,
                m_sender_name=profile_info.get("real_name") or profile_info.get("username") or target_username,
                m_url=target_url,
                m_message_sharable_link=target_url,
                m_weblink=[target_url],
                m_network="clearnet",
                m_content=profile_info.get("bio"),
                m_content_type=["social_collector", "instagram_profile", "profile_info"],
                m_date=datetime.now().date(),
                m_channel_url=target_url,
                m_message_id=target_username,
                m_platform=[self.platform],
                m_group_name=profile_info.get("username") or target_username,
                m_group_info=profile_info.get("group_info") or None,
                m_img_src=profile_info.get("profileIcon") or None,
                m_coverpage=profile_info.get("coverpage") or None,
                m_scrap_file=self.__class__.__name__,
            )
            self.append_leak_data(card_data, entity_model(m_username=[target_username] if target_username else []))
            return

        try:
            page.goto(self.m_seed_url, wait_until="domcontentloaded", timeout=25000)
        except Exception:
            pass
        page.wait_for_timeout(random.randint(1000, 2500))
        current_url = (page.url or "").lower()
        is_login_redirect = "/accounts/login/" in current_url and f"%2f{target_username.lower()}%2f" in current_url
        if is_login_redirect:
            self._last_status = "auth_required"
            self._last_reason = "instagram redirected the public profile to login"
        if self._is_wrong_profile_page(page, target_username) and not is_login_redirect:
            self._clear_browser_session(page)
            try:
                page.goto(self.m_seed_url, wait_until="domcontentloaded", timeout=25000)
            except Exception:
                pass
        page.wait_for_timeout(random.randint(1000, 10000))

        profile_assets = self._extract_profile_assets(page)
        if is_profile_request and profile_assets.get("profileIcon"):
            fallback = page.evaluate("""() => {
                const first = selectors => {
                    for (const selector of selectors) {
                        const node = document.querySelector(selector);
                        const value = node?.getAttribute('content') || node?.innerText || '';
                        if (value) return String(value).replace(/\\s+/g, ' ').trim();
                    }
                    return '';
                };
                return {
                    title: first(['meta[property="og:title"]', 'meta[name="twitter:title"]']) || document.title || '',
                    description: first(['meta[property="og:description"]', 'meta[name="description"]']) || document.body?.innerText?.slice(0, 500) || ''
                };
            }""") or {}
            title = helper_method.scalar_text(fallback.get("title")) or target_username
            description = helper_method.scalar_text(fallback.get("description"))
            card_data = social_model(
                m_title=title,
                m_sender_name=target_username,
                m_url=target_url,
                m_message_sharable_link=target_url,
                m_weblink=[target_url],
                m_network="clearnet",
                m_content=description,
                m_content_type=["social_collector", "instagram_profile", "profile_info"],
                m_date=datetime.now().date(),
                m_channel_url=target_url,
                m_message_id=target_username,
                m_platform=[self.platform],
                m_group_name=target_username,
                m_group_info=description or None,
                m_img_src=profile_assets.get("profileIcon") or None,
                m_coverpage=profile_assets.get("coverpage") or None,
                m_scrap_file=self.__class__.__name__,
            )
            self._last_status = self._last_status or "ok"
            self._last_reason = self._last_reason or "instagram public profile metadata returned profile image"
            self.append_leak_data(card_data, entity_model(m_username=[target_username] if target_username else []))
            return
        if not web_profile_data:
            web_profile_data = self._fetch_web_profile_info(page, target_username, allow_tor=False)
        if web_profile_data:
            profile_info = self._profile_info_from_web_profile(web_profile_data, target_username, profile_assets)
            if self._is_profile_data_type(data_type):
                content_type = "profile_info"
                card_data = social_model(
                    m_title=profile_info.get("username") or target_username,
                    m_sender_name=profile_info.get("real_name") or profile_info.get("username") or target_username,
                    m_url=target_url,
                    m_message_sharable_link=target_url,
                    m_weblink=[target_url],
                    m_network="clearnet",
                    m_content=profile_info.get("bio"),
                    m_content_type=["social_collector", "instagram_profile", content_type],
                    m_date=datetime.now().date(),
                    m_channel_url=target_url,
                    m_message_id=target_username,
                    m_platform=[self.platform],
                    m_group_name=profile_info.get("username") or target_username,
                    m_group_info=profile_info.get("group_info") or None,
                    m_img_src=profile_info.get("profileIcon") or None,
                    m_coverpage=profile_info.get("coverpage") or None,
                    m_scrap_file=self.__class__.__name__,
                )
                self.append_leak_data(card_data, entity_model(m_username=[target_username] if target_username else []))
                return

            if data_type != SocialDataType.COMMENTS:
                items = self._extract_grid_items_from_web_profile(page, target_username, posts_limit, web_profile_data, allow_tor=False)
                for item in items:
                    item_date = None
                    if item.get("time"):
                        try:
                            item_date = datetime.fromisoformat(str(item["time"]).replace("Z", "+00:00")).date()
                        except Exception:
                            item_date = None
                    item_type = helper_method.scalar_text(item.get("type")) or "post"
                    post_url = helper_method.scalar_text(item.get("post_url")) or target_url
                    card_data = social_model(
                        m_title=profile_info.get("username") or target_username,
                        m_sender_name=profile_info.get("real_name") or profile_info.get("username") or target_username,
                        m_url=post_url,
                        m_message_sharable_link=post_url,
                        m_weblink=[post_url],
                        m_network="clearnet",
                        m_content=helper_method.scalar_text(item.get("caption")),
                        m_content_type=["social_collector", f"instagram_{item_type}", "posts"],
                        m_date=item_date,
                        m_channel_url=target_url,
                        m_platform=[self.platform],
                        m_group_name=profile_info.get("username") or target_username,
                        m_group_info=profile_info.get("bio") or None,
                        m_comments=[],
                        m_post_likes=helper_method.scalar_text(item.get("likes", "0")),
                        m_comment_count=helper_method.scalar_text(item.get("comment_count")),
                        m_img_src=helper_method.scalar_text(item.get("media")) or None,
                        m_message_id=helper_method.scalar_text(item.get("post_id")),
                        m_scrap_file=self.__class__.__name__,
                    )
                    self.append_leak_data(card_data, entity_model(m_team="instagram_scraper"))
                if items:
                    self._last_status = "ok"
                    self._last_reason = "instagram web profile endpoint returned media edges"
                    return
                if not self._last_status:
                    self._last_status = "no_public_posts"
                    self._last_reason = "instagram web profile data did not include media edges"

        try:
            page.wait_for_selector("header", timeout=10000)
        except Exception:
            if not self._is_profile_data_type(data_type):
                self._dismiss_login_modal(page)
                items = self._extract_grid_items_from_page(
                    page=page,
                    target_username=target_username,
                    content_type="post",
                    limit=posts_limit,
                    max_comments=comments_per_post,
                    comment_offset=self._comment_offset(),
                )
                for item in items:
                    item_date = None
                    if item.get("time"):
                        try:
                            item_date = datetime.fromisoformat(str(item["time"]).replace("Z", "+00:00")).date()
                        except Exception:
                            item_date = None
                    item_type = helper_method.scalar_text(item.get("type")) or "post"
                    post_url = helper_method.scalar_text(item.get("post_url")) or target_url
                    card_data = social_model(
                        m_title=target_username,
                        m_sender_name=target_username,
                        m_url=post_url,
                        m_message_sharable_link=post_url,
                        m_weblink=[post_url],
                        m_network="clearnet",
                        m_content=helper_method.scalar_text(item.get("caption")),
                        m_content_type=["social_collector", f"instagram_{item_type}", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                        m_date=item_date,
                        m_channel_url=target_url,
                        m_platform=[self.platform],
                        m_group_name=target_username,
                        m_comments=[],
                        m_post_likes=helper_method.scalar_text(item.get("likes", "0")),
                        m_comment_count=helper_method.scalar_text(item.get("comment_count")) if data_type == SocialDataType.COMMENTS else None,
                        m_img_src=helper_method.scalar_text(item.get("media")) or None,
                        m_message_id=helper_method.scalar_text(item.get("post_id")),
                        m_scrap_file=self.__class__.__name__,
                    )
                    self.append_leak_data(card_data, entity_model(m_team="instagram_scraper"))
                if items:
                    self._last_status = "ok"
                    self._last_reason = "instagram DOM fallback returned grid items"
                elif not self._last_status:
                    self._last_status = "no_public_posts"
                    self._last_reason = "instagram DOM fallback found no public grid items"
                return
            profile_assets = self._extract_profile_assets(page)
            fallback = page.evaluate("""() => {
                const first = selectors => {
                    for (const selector of selectors) {
                        const node = document.querySelector(selector);
                        const value = node?.getAttribute('content') || node?.innerText || '';
                        if (value) return String(value).replace(/\\s+/g, ' ').trim();
                    }
                    return '';
                };
                return {
                    title: first(['meta[property="og:title"]', 'meta[name="twitter:title"]']) || document.title || '',
                    description: first(['meta[property="og:description"]', 'meta[name="description"]']) || document.body?.innerText?.slice(0, 500) || ''
                };
            }""") or {}
            content_type = "profile_info"
            title = helper_method.scalar_text(fallback.get("title")) or target_username
            card_data = social_model(
                m_title=title,
                m_sender_name=target_username,
                m_url=target_url,
                m_message_sharable_link=target_url,
                m_weblink=[target_url],
                m_network="clearnet",
                m_content=helper_method.scalar_text(fallback.get("description")),
                m_content_type=["social_collector", "instagram_profile", content_type],
                m_date=datetime.now().date(),
                m_channel_url=target_url,
                m_message_id=target_username,
                m_platform=[self.platform],
                m_group_name=target_username,
                m_img_src=profile_assets.get("profileIcon") or None,
                m_coverpage=profile_assets.get("coverpage") or None,
                m_scrap_file=self.__class__.__name__,
            )
            self.append_leak_data(card_data, entity_model(m_username=[target_username] if target_username else []))
            return

        username_loc = page.locator("header h2, header span._ap3a").filter(visible=True)
        username = username_loc.first.inner_text() if username_loc.count() > 0 else ""
        real_name_loc = page.locator("header section h1, header section span[dir='auto']").filter(visible=True)
        real_name = real_name_loc.first.inner_text() if real_name_loc.count() > 0 else ""
        bio_loc = page.locator("header section span._ap3a._aaco._aacu._aacx._aad7._aade[dir='auto']").filter(
            visible=True)
        raw_bio_text = bio_loc.first.inner_text() if bio_loc.count() > 0 else ""
        bio_text = raw_bio_text.replace("... more", "").replace("\nmore", "").strip() if raw_bio_text else ""
        header_text = page.locator("header").first.inner_text() if page.locator("header").count() > 0 else ""
        profile_assets = self._extract_profile_assets(page)

        if self._is_profile_data_type(data_type):
            content_type = "profile_info"
            card_data = social_model(
                m_title=username or target_username,
                m_sender_name=real_name or username or target_username,
                m_url=target_url,
                m_message_sharable_link=target_url,
                m_weblink=[target_url],
                m_network="clearnet",
                m_content=bio_text,
                m_content_type=["social_collector", "instagram_profile", content_type],
                m_date=datetime.now().date(),
                m_channel_url=target_url,
                m_message_id=target_username,
                m_platform=[self.platform],
                m_group_name=username or target_username,
                m_group_info=header_text or None,
                m_img_src=profile_assets.get("profileIcon") or None,
                m_coverpage=profile_assets.get("coverpage") or None,
                m_scrap_file=self.__class__.__name__,
            )
            self.append_leak_data(card_data, entity_model(m_username=[target_username] if target_username else []))
            return

        def on_item(item):
            item_date = None
            if item.get("time"):
                try:
                    item_date = datetime.fromisoformat(item["time"].replace("Z", "+00:00")).date()
                except Exception:
                    item_date = None

            item_comments: List[social_comment_model] = []
            for comment in item.get("comments", []):
                if comment.get("text"):
                    item_comments.append(
                        social_comment_model(
                            m_username=helper_method.scalar_text(comment.get("username")) or None,
                            m_time=helper_method.scalar_text(item.get("time")) or None,
                            m_text=helper_method.scalar_text(comment.get("text")) or None,
                        )
                    )

            item_type = helper_method.scalar_text(item.get("type")) or "social_collector"
            post_url = helper_method.scalar_text(item.get("post_url")) or target_url

            card_data = social_model(
                m_title=username,
                m_sender_name=real_name,
                m_url=post_url,
                m_message_sharable_link=post_url,
                m_weblink=[post_url],
                m_network="clearnet",
                m_content=helper_method.scalar_text(item.get("caption")),
                m_content_type=["social_collector", f"instagram_{item_type}", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                m_date=item_date,
                m_channel_url=target_url,
                m_platform=[self.platform],
                m_group_name=username,
                m_group_info=bio_text,
                m_comments=item_comments,
                m_post_likes=helper_method.scalar_text(item.get("likes", "0")),
                m_comment_count=(
                    str(len(item_comments)) if item_comments
                    else helper_method.scalar_text(item.get("comment_count"))
                ) if data_type == SocialDataType.COMMENTS else None,
                m_commenters=list({comment.m_username for comment in item_comments if comment.m_username}),
                m_img_src=helper_method.scalar_text(item.get("media")) or None,
                m_message_id=helper_method.scalar_text(item.get("post_id")),
                m_scrap_file=self.__class__.__name__,
            )

            entity_data = entity_model(
                m_team="instagram_scraper",
            )

            self.append_leak_data(card_data, entity_data)

        before_count = len(self._card_data)
        self.extract_grid_items(
            page=page,
            target_username=target_username,
            content_selector="main a[href*='/p/'], main a[href*='/reel/']",
            content_type="post",
            limit=posts_limit,
            max_comments=comments_per_post,
            comment_offset=self._comment_offset(),
            on_item=on_item
        )
        if len(self._card_data) > before_count:
            self._last_status = "ok"
            self._last_reason = "instagram DOM grid returned posts"
        elif not self._last_status:
            self._last_status = "no_public_posts"
            self._last_reason = "instagram public page exposed no post grid"
