import difflib

from ddgs import DDGS
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse
from datetime import datetime, timezone

from api.social_manager.social_enums import SITE_DATA


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

    def collect_social_handles(self, query: str, threshold: float = 0) -> Dict[str, Any]:
        query = f'"{query}" social profile'
        sites = {site.lower() for site in SITE_DATA.ALL_SITES}

        results: List[Dict[str, Any]] = []
        seen_profiles: set[str] = set()
        query_lower = query.lower().strip()
        try:
            with DDGS() as ddgs:
                text_results = ddgs.text(f"{query} social media profile", max_results=30)
                for r in text_results:
                    url = r.get("href", "")
                    if not url:
                        continue
                    platform = self.extract_platform_from_url(url)
                    if platform is None:
                        continue
                    parsed = urlparse(url)
                    platform_url = f"{parsed.scheme}://{parsed.netloc}/"
                    username = self.extract_username_from_url(url)
                    if username is None:
                        continue
                    similarity = difflib.SequenceMatcher(None, username.lower(), query_lower).ratio()
                    if similarity < threshold:
                        continue
                    profile_key = f"{platform}:{username}"
                    if profile_key in seen_profiles:
                        continue
                    seen_profiles.add(profile_key)

                    if platform in sites:
                        results.append({
                            "metadata": {
                                "status": "suggested",
                                "platform": platform,
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

    def scrape_usernames(self, username: str, platform: str, limit: int = 10) -> Dict[str, Any]:
        platform = (platform or "").lower().strip()
        platform_domain = f"{platform}.com" if platform and not platform.endswith(".com") else platform
        search_query = f'site:{platform_domain} "{username}"'
        profiles = []
        seen_usernames = set()
        try:
            with DDGS() as ddgs:
                text_results = ddgs.text(search_query, max_results=limit * 3)
                for r in text_results:
                    if len(profiles) >= limit:
                        break
                    url = r.get("href")
                    if not url or platform_domain not in url:
                        continue
                    extracted_username = self.extract_username_from_url(url)
                    if not extracted_username or extracted_username in seen_usernames:
                        continue
                    seen_usernames.add(extracted_username)
                    profiles.append({
                        "username": extracted_username,
                        "real_name": self.extract_real_name(r.get("title", "")),
                        "profile_url": url,
                        "title": r.get("title", ""),
                        "snippet": r.get("body", ""),
                        "platform": platform,
                    })
            return {
                "searched_username": username,
                "platform": platform,
                "total_found": len(profiles),
                "usernames": list(seen_usernames),
                "profiles": profiles,
            }
        except Exception as e:
            return {
                "searched_username": username,
                "platform": platform,
                "error": str(e),
                "total_found": 0,
                "usernames": [],
                "profiles": [],
            }

    def scrape_images(self, username: str, platform: str, limit: int = 10) -> Dict[str, Any]:
        platform = (platform or "").lower().strip()
        search_query = f"{username} {platform}"
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

    def search_web(self, query: str) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        try:
            with DDGS() as ddgs:
                text_results = ddgs.text(query, max_results=20)
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
