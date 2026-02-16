import asyncio
import difflib

from PicImageSearch import Yandex
from ddgs import DDGS
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse
from datetime import datetime, timezone
from api.social_manager.social_enums import SITE_DATA
import tldextract

class live_search_handler:
    def __init__(self) -> None:
        self.timestamp = datetime.now(timezone.utc).isoformat()

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
    def extract_username_from_url(url: str) -> Optional[str]:
        try:
            parsed = urlparse(url)
            path = parsed.path.strip("/")
            if not path:
                return None
            if path.startswith("@"):
                return path.replace("@", "").split("/")[0] or None
            parts = path.split("/")
            if "in" in parts:
                idx = parts.index("in")
                if idx + 1 < len(parts):
                    return parts[idx + 1] or None
            if "@" in path and path.count("@") == 1:
                username = path.split("@", 1)[1].split("/")[0]
                return username or None
            username = parts[0] if parts else None
            excluded = [
                "search", "explore", "hashtag", "tag", "p", "reel", "post",
                "status", "posts", "about", "help", "support", "privacy",
                "terms", "settings", "home", "feed", "trending", "login",
                "signup", "register", "watch", "video", "channel", "user",
                "c", "orgs", "features", "pricing",
            ]
            if username and not any(keyword in username.lower() for keyword in excluded):
                return username
            return None
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

    def collect_social_handles(self, query: str, platform: Optional[str] = None, threshold: float = 0) -> Dict[
        str, Any]:
        platform_clean = platform.lower().strip() if platform and platform.lower().strip() not in ("string", "none",
                                                                                                   "") else None

        search_query = f'site:{platform_clean}.com "{query}"' if platform_clean else f'"{query}" social profile'

        sites = {site.lower() for site in SITE_DATA.ALL_SITES}
        results: List[Dict[str, Any]] = []
        seen_profiles: set[str] = set()
        query_lower = query.lower().strip()

        try:
            with DDGS() as ddgs:
                text_results = ddgs.text(search_query, max_results=30)
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
                    username = self.extract_username_from_url(url)
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

    def extract_accounts_from_image(self, image_path: str, threshold: float = 0.0) -> list[dict]:
        print("0:::::::::::::::::::::::::::::::", flush=True)
        print("0:::::::::::::::::::::::::::::::", flush=True)
        sites = {site.lower() for site in SITE_DATA.ALL_SITES}
        results = []

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            yandex = Yandex()
            resp = loop.run_until_complete(yandex.search(file=image_path))
            loop.close()

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

            print("1:::::::::::::::::::::::::::::::", flush=True)
            print("1:::::::::::::::::::::::::::::::", flush=True)
            print(results, flush=True)
            print("1:::::::::::::::::::::::::::::::", flush=True)
            print("1:::::::::::::::::::::::::::::::", flush=True)
            return results

        except Exception as ex:
            print("2:::::::::::::::::::::::::::::::", flush=True)
            print(ex, flush=True)
            print("2:::::::::::::::::::::::::::::::", flush=True)
            return []

    def scrape_images(self, username: str, platform: str, limit: int = 10) -> Dict[str, Any]:
        platform = (platform or "").lower().strip()
        search_query = f'site:{platform}.com "{username}"'

        image_results = []
        try:
            with DDGS() as ddgs:
                image_search_results = ddgs.images(search_query, max_results=limit)
                for img in image_search_results:
                    image_url = img.get("image")
                    if image_url:
                        image_results.append({
                            "image_url": image_url,
                            "thumbnail": img.get("thumbnail"),
                            "title": img.get("title"),
                            "source": img.get("source"),
                        })
            return {
                "searched_username": username,
                "platform": platform,
                "total_found": len(image_results),
                "images": image_results,
            }
        except Exception as e:
            return {
                "searched_username": username,
                "platform": platform,
                "error": str(e),
                "total_found": 0,
                "images": [],
            }

    def check_username_exists(self, username: str, platform: str) -> bool:
        platform = platform.lower().strip()
        username_lower = username.lower()
        try:
            with DDGS() as ddgs:
                search_query = f'site:{platform}.com "{username}"'
                text_results = ddgs.text(search_query, max_results=10)
                for r in text_results:
                    url = r.get("href", "").lower()
                    if not url or f"{platform}.com" not in url:
                        continue
                    if username_lower in url:
                        return True
            return False
        except Exception:
            return False

    def search_web(self, query: str, platform: Optional[str] = None) -> Dict[str, Any]:
        search_query = f'site:{platform.lower().strip()}.com {query}' if platform else query
        results: List[Dict[str, Any]] = []

        try:
            with DDGS() as ddgs:
                text_results = ddgs.text(search_query, max_results=20)
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

    def scrape_profile(self, username: str, platform: Optional[str] = None) -> Dict[str, Any]:
        platform_clean = (platform or "").lower().strip()

        if platform_clean:
            search_query = f'{username} {platform_clean} profile'
        else:
            search_query = f'{username} social media profile'

        try:
            with DDGS() as ddgs:
                text_results = ddgs.text(search_query, max_results=15)
                for r in text_results:
                    url = r.get("href", "")
                    if not url:
                        continue
                    extracted_platform = self.extract_platform_from_url(url)
                    if not extracted_platform:
                        continue
                    if platform_clean and extracted_platform != platform_clean:
                        continue
                    if username.lower() not in url.lower():
                        continue
                    extracted_username = self.extract_username_from_url(url)
                    if not extracted_username:
                        extracted_username = username
                    parsed = urlparse(url)
                    profile_url = f"{parsed.scheme}://{parsed.netloc}/{extracted_username}"
                    title = r.get("title", "")
                    snippet = r.get("body", "")
                    real_name = self.extract_real_name(title)
                    return {
                        "profile": {
                            "real_name": real_name or "",
                            "bio": snippet or "",
                            "location": "",
                            "total_posts": "",
                            "total_followers": "",
                            "total_following": "",
                            "profile_url": profile_url,
                        },
                        "platform": extracted_platform,
                        "username": extracted_username,
                        "status": "suggested",
                    }
            return {
                "profile": None,
                "platform": platform_clean,
                "username": username,
                "status": "suggested",
            }
        except Exception:
            return {
                "profile": None,
                "platform": platform_clean,
                "username": username,
                "status": "suggested",
            }

    def scrape_posts_search(self, username: str, platform: Optional[str] = None, max_posts: int = 10) -> Dict[str, Any]:
        platform_str = (platform or "").lower().strip()
        if platform_str:
            search_query = f'site:{platform_str}.com "{username}" posts OR status OR video'
        else:
            search_query = f'"{username}" posts OR status OR video social'
        posts = []
        try:
            with DDGS() as ddgs:
                text_results = ddgs.text(search_query, max_results=max_posts * 2)
                for r in text_results:
                    if len(posts) >= max_posts:
                        break
                    url = r.get("href", "")
                    if not url:
                        continue
                    posts.append({
                        "status": "suggested",
                        "post_url": url,
                        "datetime": None,
                        "caption": r.get("body", ""),
                        "media_url": None,
                        "media_type": None,
                        "comments": "0",
                        "likes": "0",
                        "retweets": None,
                        "views": None,
                    })
            return {
                "username": username,
                "platform": platform_str,
                "posts": posts,
                "total_count": len(posts),
                "status": "suggested",
            }
        except Exception as e:
            return {
                "username": username,
                "platform": platform_str,
                "posts": [],
                "total_count": 0,
                "error": str(e),
                "status": "suggested",
            }
