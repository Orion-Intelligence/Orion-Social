import asyncio
import difflib
import hashlib
import os
import re

import tldextract
from ddgs import DDGS
from ddgs.exceptions import DDGSException
from typing import Dict, Any, Optional, List, Tuple
from urllib.parse import urlparse
from datetime import datetime, timezone

from api.social_manager.social_enums import SITE_DATA

try:
    from PicImageSearch import Yandex
except ModuleNotFoundError:
    Yandex = None


class live_search_handler:
    def __init__(self) -> None:
        self.timestamp = datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _tor_proxy_url() -> str:
        return (
            os.getenv("TOR_IMAGE_PROXY_URL")
            or os.getenv("TOR_PROXY_URL")
            or "socks5h://trusted-social_tor_instace_1:9552"
        )

    def _ddgs(self) -> DDGS:
        return DDGS(proxy=self._tor_proxy_url())

    @staticmethod
    def _direct_fallback_enabled() -> bool:
        return os.getenv("TOR_IMAGE_DIRECT_FALLBACK", "true").lower() not in {"0", "false", "no"}

    @staticmethod
    def _is_resolution_error(exc: Exception) -> bool:
        msg = str(exc).lower()
        return (
            "temporary failure in name resolution" in msg
            or "failed to lookup address information" in msg
            or "could not contact dns servers" in msg
        )

    @staticmethod
    def _should_retry_direct(exc: Exception) -> bool:
        msg = str(exc).lower()
        return (
            (
                isinstance(exc, DDGSException)
                or live_search_handler._is_resolution_error(exc)
            )
            and (
                "error sending request" in msg
                or "timed out" in msg
                or "proxy" in msg
                or "no results found" in msg
                or "temporary failure in name resolution" in msg
                or "failed to lookup address information" in msg
                or "could not contact dns servers" in msg
            )
        )

    def _ddgs_search(self, method: str, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        try:
            with self._ddgs() as ddgs:
                return getattr(ddgs, method)(query, **kwargs)
        except Exception as exc:
            if not self._direct_fallback_enabled() or not self._should_retry_direct(exc):
                return []
            try:
                with DDGS() as ddgs:
                    return getattr(ddgs, method)(query, **kwargs)
            except Exception:
                return []

    def _search_yandex(self, image_path: str):
        if Yandex is None:
            return None

        try:
            yandex = Yandex(proxies=self._tor_proxy_url())
            return asyncio.run(yandex.search(file=image_path))
        except Exception:
            if not self._direct_fallback_enabled():
                raise
            yandex = Yandex()
            return asyncio.run(yandex.search(file=image_path))

    @staticmethod
    def extract_platform_from_url(url: str) -> Optional[str]:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower().replace("www.", "")
            if "." in domain:
                parts = domain.split(".")
                if len(parts) >= 2:
                    return parts[-2]
            return None
        except Exception:
            return None

    @staticmethod
    def extract_username_from_url(url: str, query: str = "") -> Optional[str]:
        try:
            parsed = urlparse(url)
            path = parsed.path.strip("/")
            if not path:
                return None

            excluded = {
                "search", "explore", "hashtag", "tag", "p", "reel", "post",
                "status", "posts", "about", "help", "support", "privacy",
                "terms", "settings", "home", "feed", "trending", "login",
                "signup", "register", "watch", "video", "videos", "channel",
                "user", "c", "orgs", "features", "pricing", "stories", "in",
                "highlights", "saved", "tagged", "reels", "live",
            }

            parts = [p.lstrip("@") for p in path.split("/") if p and p.lstrip("@") not in excluded]

            if not parts:
                return None

            if not query:
                return parts[0]

            query_lower = query.lower().replace(" ", "").strip()

            best_token = None
            best_score = -1.0

            for token in parts:
                token_lower = token.lower()
                score = difflib.SequenceMatcher(None, token_lower, query_lower).ratio()
                if score > best_score:
                    best_score = score
                    best_token = token

            return best_token

        except Exception:
            return None

    @staticmethod
    def extract_real_name(title: str) -> Optional[str]:
        if not title:
            return None
        title_clean = title.strip()
        if len(title_clean) <= 2:
            return None
        delimiters = ["(", " - ", " | ", "@", "•", "–", ":"]
        for delim in delimiters:
            if delim in title_clean:
                real_name = title_clean.split(delim, 1)[0].strip()
                if len(real_name) > 2:
                    return real_name
        return title_clean

    def collect_social_handles(self, query: str, platform: Optional[str] = None, threshold: float = 0) -> Dict[str, Any]:
        platform_clean = platform.lower().strip() if platform and platform.lower().strip() not in ("string", "none",
                                                                                                   "") else None

        search_query = f'site:{platform_clean}.com "{query}"' if platform_clean else f'"{query}" social profile'

        sites = {site.lower() for site in SITE_DATA.ALL_SITES}
        results: List[Dict[str, Any]] = []
        seen_profiles: set[str] = set()
        query_lower = query.lower().strip()

        try:
            text_results = self._ddgs_search("text", search_query, max_results=30)
            for r in text_results:
                url = r.get("href", "")
                if not url:
                    continue
                extracted_platform = self.extract_platform_from_url(url)
                if extracted_platform is None:
                    continue
                if platform_clean and extracted_platform != platform_clean:
                    continue
                parsed = urlparse(url)
                platform_url = f"{parsed.scheme}://{parsed.netloc}/"
                username = self.extract_username_from_url(url, query=query)

                if username is None:
                    continue
                similarity = difflib.SequenceMatcher(None, username.lower(), query_lower).ratio()
                if similarity < threshold:
                    continue
                profile_key = f"{extracted_platform}:{username}"
                if profile_key in seen_profiles:
                    continue
                seen_profiles.add(profile_key)
                if platform_clean or extracted_platform in sites:
                    results.append({
                        "metadata": {
                            "platform": extracted_platform,
                            "username": username,
                            "social_handle": username,
                            "url": platform_url,
                            "timestamp": self.timestamp,
                        },
                        "data": {
                            "title": r.get("title", ""),
                            "snippet": r.get("body", ""),
                            "real_name": self.extract_real_name(r.get("title", "")),
                        },
                    })
            return {
                "query": query,
                "total_found": len(results),
                "timestamp": self.timestamp,
                "results": results,
            }
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "total_found": 0,
                "timestamp": self.timestamp,
                "results": [],
            }


    @staticmethod
    def _split_username(username: str) -> str:
        name = username.replace("_", " ").replace("-", " ").replace(".", " ")
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
        name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', name)
        return " ".join(name.split())

    def _build_image_queries(self, username: str, platform: str) -> List[str]:
        queries = []
        username = (username or "").strip()
        platform = (platform or "").lower().strip()
        if platform == "reddit":
            reddit_handle = username.strip("/")
            reddit_handle_lower = reddit_handle.lower()
            if reddit_handle_lower.startswith("r/"):
                subreddit = reddit_handle[2:].strip("/")
                return [
                    f'site:reddit.com/r/{subreddit} "{subreddit}"',
                    f'"r/{subreddit}" reddit',
                    f'reddit.com/r/{subreddit} images',
                    f'{subreddit} subreddit images',
                ]
            if reddit_handle_lower.startswith("u/"):
                reddit_user = reddit_handle[2:].strip("/")
                return [
                    f'site:reddit.com/user/{reddit_user} "{reddit_user}"',
                    f'"u/{reddit_user}" reddit',
                    f'reddit.com/user/{reddit_user} images',
                    f'{reddit_user} reddit profile images',
                ]
            if reddit_handle_lower.startswith("user/"):
                reddit_user = reddit_handle[5:].strip("/")
                return [
                    f'site:reddit.com/user/{reddit_user} "{reddit_user}"',
                    f'"u/{reddit_user}" reddit',
                    f'reddit.com/user/{reddit_user} images',
                    f'{reddit_user} reddit profile images',
                ]
        split_name = self._split_username(username)
        has_split = split_name.lower() != username.lower()

        if platform:
            queries.append(f'"{username}" {platform}')
            if has_split:
                queries.append(f'"{split_name}" {platform}')
            queries.append(f'{username} {platform} photo')
            if has_split:
                queries.append(f'{split_name} {platform} photo')
        else:
            queries.append(f'"{username}"')
            if has_split:
                queries.append(f'"{split_name}"')
            queries.append(f'{username} photo')

        return queries

    def _image_search(self, queries: List[str], limit: int) -> Tuple[List[Dict], set]:
        seen_urls: set[str] = set()
        results = []
        for query in queries:
            if len(results) >= limit:
                break
            try:
                for img in self._ddgs_search("images", query, max_results=limit - len(results)):
                    image_url = img.get("image")
                    if image_url and image_url not in seen_urls:
                        seen_urls.add(image_url)
                        results.append({
                            "image_url": image_url,
                            "thumbnail": img.get("thumbnail"),
                            "title": img.get("title"),
                            "source": img.get("source"),
                        })
            except Exception:
                continue
        return results, seen_urls

    def _text_image_fallback(self, username: str, platform: str, limit: int, seen_urls: set) -> List[Dict]:
        split_name = self._split_username(username)
        queries = [
            f'{username} {platform} photos' if platform else f'{username} photos',
            f'{split_name} {platform} images' if platform else f'{split_name} images',
        ]
        results = []
        for query in queries:
            if len(results) >= limit:
                break
            try:
                for r in self._ddgs_search("text", query, max_results=limit * 2):
                    if len(results) >= limit:
                        break
                    image_url = r.get("image", "")
                    href = r.get("href", "")
                    url = image_url or href
                    if not url or url in seen_urls:
                        continue
                    if image_url or re.search(r'\.(jpg|jpeg|png|webp)', url, re.IGNORECASE):
                        seen_urls.add(url)
                        results.append({
                            "image_url": url,
                            "thumbnail": image_url or "",
                            "title": r.get("title", ""),
                            "source": href,
                        })
            except Exception:
                continue
        return results

    @staticmethod
    def _image_hash(image: Dict[str, Any]) -> str:
        raw_hash = "|".join([
            str(image.get("image_url") or ""),
            str(image.get("thumbnail") or ""),
            str(image.get("source") or ""),
            str(image.get("title") or ""),
        ])
        return hashlib.sha256(raw_hash.encode("utf-8")).hexdigest()

    def _add_image_hashes(self, images: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for image in images:
            image["hash_id"] = self._image_hash(image)
        return images

    @staticmethod
    def _cut_images_by_hash(images: List[Dict[str, Any]], hash_id: str | None) -> List[Dict[str, Any]]:
        if not hash_id:
            return images
        for index, image in enumerate(images):
            if image.get("hash_id") == hash_id:
                return images[:index]
        return images

    def scrape_images(self, username: str, platform: str, limit: int = 10, hash_id: str | None = None) -> Dict[str, Any]:
        platform = (platform or "").lower().strip()
        limit = max(1, min(int(limit or 10), 100))
        queries = self._build_image_queries(username, platform)

        image_results, seen_urls = self._image_search(queries, limit)

        if len(image_results) < limit:
            image_results.extend(
                self._text_image_fallback(username, platform, limit - len(image_results), seen_urls)
            )

        image_results = self._cut_images_by_hash(self._add_image_hashes(image_results), hash_id)
        return {
            "searched_username": username,
            "platform": platform,
            "total_found": len(image_results),
            "images": image_results,
        }

    def extract_accounts_from_image(self, image_path: str) -> list[dict]:
        sites = {site.lower() for site in SITE_DATA.ALL_SITES}
        results = []

        try:
            resp = self._search_yandex(image_path)

            raw = getattr(resp, "raw", None) or []
            pages = []

            for item in raw:
                u = (
                    item.get("url") or item.get("link") or item.get("source") or ""
                    if isinstance(item, dict)
                    else getattr(item, "url", "") or getattr(item, "link", "") or getattr(item, "source", "") or ""
                )
                if u:
                    pages.append(u)
            seen = set()

            for url in pages:
                parsed = urlparse(url)
                base_url = f"{parsed.scheme}://{parsed.netloc}/"

                platform = self.extract_platform_from_url(url)
                username = self.extract_username_from_url(url)

                if platform and platform.lower() in sites:
                    social_handle = platform
                else:
                    ext = tldextract.extract(parsed.netloc)
                    if not ext.domain or not ext.suffix:
                        continue
                    platform = f"{ext.domain}.{ext.suffix}"
                    social_handle = ""

                ident = (username or social_handle or "").lower()
                if not ident:
                    continue

                key = f"{platform}:{ident}"
                if key in seen:
                    continue
                seen.add(key)

                results.append({
                    "metadata": {
                        "platform": platform,
                        "username": username or "",
                        "social_handle": social_handle,
                        "url": base_url,
                        "timestamp": self.timestamp,
                        "image_path": image_path,
                    },
                    "data": {
                        "title": "",
                        "snippet": "",
                        "real_name": None,
                        "matched_page": url,
                    },
                })

            return results

        except Exception:
            return []

    def search_web(self, tokens: List[str], username: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
        if not tokens:
            raise ValueError("At least one token must be provided.")

        query_parts = list(tokens)
        if username:
            query_parts.append(username)

        query = " ".join(query_parts)
        search_query = f'site:{platform.lower().strip()}.com {query}' if platform else query

        results: List[Dict[str, Any]] = []
        try:
            text_results = self._ddgs_search("text", search_query, max_results=20)
            for r in text_results:
                url = r.get("href", "")
                if not url:
                    continue
                results.append({
                    "title": r.get("title", ""),
                    "url": url,
                    "snippet": r.get("body", ""),
                    "timestamp": self.timestamp,
                })
            return {
                "query": query,
                "total_found": len(results),
                "timestamp": self.timestamp,
                "results": results,
            }
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "total_found": 0,
                "timestamp": self.timestamp,
                "results": [],
            }
