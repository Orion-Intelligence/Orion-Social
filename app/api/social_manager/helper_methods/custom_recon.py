import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlparse
from urllib.request import Request, urlopen


class custom_recon:
    REQUEST_TIMEOUT = 5
    MAX_RESPONSE_BYTES = 64_000
    MAX_WORKERS = 8
    USER_AGENT = "Mozilla/5.0 (compatible; Orion-Social-Recon/1.0)"

    PLATFORM_ORDER = (
        "discord",
        "facebook",
        "instagram",
        "linkedin",
        "mastodon",
        "pastebin",
        "reddit",
        "tiktok",
        "twitter",
        "whatsapp",
        "youtube",
    )

    PLATFORM_NAMES = {
        "discord": "Discord",
        "facebook": "Facebook",
        "instagram": "Instagram",
        "linkedin": "LinkedIn",
        "mastodon": "Mastodon",
        "pastebin": "Pastebin",
        "reddit": "Reddit",
        "tiktok": "TikTok",
        "twitter": "Twitter",
        "whatsapp": "WhatsApp",
        "youtube": "YouTube",
    }

    PLATFORM_ALIASES = {
        "x": "twitter",
        "youtube user": "youtube",
    }

    MASTODON_KNOWN_HOSTS = (
        "mastodon.social",
        "mstdn.social",
        "mas.to",
        "mastodon.online",
        "infosec.exchange",
    )
    MASTODON_RESERVED_PATHS = {
        "about",
        "api",
        "auth",
        "deck",
        "explore",
        "home",
        "inbox",
        "interact",
        "oauth",
        "public",
        "settings",
        "share",
        "tags",
        "web",
        "well-known",
    }

    @staticmethod
    def _timestamp() -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @classmethod
    def _platform_key(cls, value: str) -> str:
        key = (value or "").strip().lower()
        return cls.PLATFORM_ALIASES.get(key, key)

    @classmethod
    def _existing_platforms(cls, existing_results: list[dict] | None) -> set[str]:
        out: set[str] = set()
        for item in existing_results or []:
            meta = (item or {}).get("metadata") or {}
            platform = cls._platform_key(meta.get("platform") or "")
            if platform:
                out.add(platform)
        return out

    @staticmethod
    def _host_without_www(host: str) -> str:
        host = (host or "").lower().split(":")[0]
        return host[4:] if host.startswith("www.") else host

    @classmethod
    def _coerce_url(cls, value: str) -> str | None:
        v = (value or "").strip()
        if re.match(r"^https?://", v, flags=re.IGNORECASE):
            return v
        if re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$", v):
            return f"https://{v}"
        return None

    @staticmethod
    def _first_path_parts(url: str) -> list[str]:
        parsed = urlparse(url)
        return [unquote(part) for part in parsed.path.split("/") if part]

    @classmethod
    def _fetch(cls, url: str, accept: str = "text/html,application/json,*/*") -> tuple[int, dict, str, str]:
        request = Request(
            url,
            headers={
                "Accept": accept,
                "User-Agent": cls.USER_AGENT,
            },
        )
        try:
            with urlopen(request, timeout=cls.REQUEST_TIMEOUT) as response:
                raw = response.read(cls.MAX_RESPONSE_BYTES)
                charset = response.headers.get_content_charset() or "utf-8"
                return response.status, dict(response.headers.items()), raw.decode(charset, errors="ignore"), response.url
        except HTTPError as exc:
            raw = exc.read(cls.MAX_RESPONSE_BYTES)
            charset = exc.headers.get_content_charset() or "utf-8"
            return exc.code, dict(exc.headers.items()), raw.decode(charset, errors="ignore"), exc.url
        except (TimeoutError, URLError, OSError):
            return 0, {}, "", url

    @staticmethod
    def _json_loads(value: str) -> dict | None:
        try:
            data = json.loads(value)
            return data if isinstance(data, dict) else None
        except Exception:
            return None

    @staticmethod
    def _clean_username(username: str) -> str:
        return (username or "").strip().strip("/").lstrip("@")

    @staticmethod
    def _has_missing_marker(body: str, markers: tuple[str, ...]) -> bool:
        body_lower = (body or "").lower()
        return any(marker in body_lower for marker in markers)

    @classmethod
    def _result(
        cls,
        platform: str,
        username: str,
        url: str,
        proof_type: str,
        status_code: int,
        final_url: str | None = None,
        extra: dict | None = None,
    ) -> dict:
        display = cls.PLATFORM_NAMES.get(platform, platform.capitalize())
        proof = {
            "type": proof_type,
            "status_code": status_code,
            "checked_url": url,
            "final_url": final_url or url,
        }
        if extra:
            proof.update(extra)
        return {
            "metadata": {
                "platform": display,
                "username": username,
                "social_handle": username,
                "url": final_url or url,
                "timestamp": cls._timestamp(),
                "status": "active",
            },
            "data": {
                "profile_existence_proof": proof,
            },
        }

    @classmethod
    def _simple_url_probe(
        cls,
        platform: str,
        username: str,
        url: str,
        missing_markers: tuple[str, ...] = (),
        required_any: tuple[str, ...] = (),
        valid_statuses: tuple[int, ...] = (200,),
        proof_type: str = "http_profile",
    ) -> dict | None:
        status, _headers, body, final_url = cls._fetch(url)
        if status not in valid_statuses:
            return None
        if missing_markers and cls._has_missing_marker(body, missing_markers):
            return None
        if required_any:
            body_lower = body.lower()
            final_lower = (final_url or "").lower()
            if not any(marker.lower() in body_lower or marker.lower() in final_lower for marker in required_any):
                return None
        return cls._result(platform, username, url, proof_type, status, final_url=final_url)

    @classmethod
    def _probe_discord(cls, username: str) -> dict | None:
        # Discord has no public username profile endpoint. Only numeric user ids can be represented as a URL.
        if not re.fullmatch(r"\d{16,22}", username or ""):
            return None
        return cls._simple_url_probe(
            "discord",
            username,
            f"https://discord.com/users/{username}",
            required_any=(username,),
            proof_type="discord_user_url",
        )

    @classmethod
    def _probe_facebook(cls, username: str) -> dict | None:
        return cls._simple_url_probe(
            "facebook",
            username,
            f"https://www.facebook.com/{username}",
            missing_markers=(
                "this content isn't available",
                "this page isn't available",
                "content isn't available right now",
                "page not found",
            ),
        )

    @classmethod
    def _probe_instagram(cls, username: str) -> dict | None:
        return cls._simple_url_probe(
            "instagram",
            username,
            f"https://www.instagram.com/{username}/",
            missing_markers=(
                "sorry, this page isn't available",
                "the link you followed may be broken",
            ),
            required_any=(f"/{username}/", f'"username":"{username}"'),
        )

    @classmethod
    def _probe_linkedin(cls, username: str) -> dict | None:
        return cls._simple_url_probe(
            "linkedin",
            username,
            f"https://www.linkedin.com/in/{username}/",
            missing_markers=("profile not found", "page not found"),
            required_any=(f"/in/{username}",),
        )

    @classmethod
    def _extract_mastodon_identity_from_url(cls, url: str) -> tuple[str | None, str | None, str | None]:
        parsed = urlparse(url)
        host = cls._host_without_www(parsed.netloc)
        parts = cls._first_path_parts(url)

        username = None
        account_host = host
        if parts:
            first = parts[0]
            if first.startswith("@") and len(first) > 1:
                username = first.lstrip("@")
            elif first == "users" and len(parts) > 1:
                username = parts[1].lstrip("@")
            elif first == "web" and len(parts) > 1 and parts[1].startswith("@"):
                username = parts[1].lstrip("@")
            elif first not in cls.MASTODON_RESERVED_PATHS and "@" not in first:
                username = first.lstrip("@")

        if not host:
            return None, None, None

        if username and "@" in username:
            username, account_host = username.split("@", 1)

        handle = f"@{username}@{account_host}" if username else host
        if username:
            account_path = f"@{username}@{account_host}" if account_host != host else f"@{username}"
            canonical_url = f"{parsed.scheme or 'https'}://{host}/{account_path}"
        else:
            canonical_url = f"{parsed.scheme or 'https'}://{host}"
        return username, handle, canonical_url.rstrip("/")

    @classmethod
    def _extract_mastodon_handle(cls, value: str) -> tuple[str, str] | None:
        match = re.match(r"^@([A-Za-z0-9_][A-Za-z0-9_.-]{0,80})@([A-Za-z0-9.-]+\.[A-Za-z]{2,})/?$", (value or "").strip())
        if not match:
            return None
        return match.group(1), match.group(2).lower()

    @classmethod
    def _mastodon_webfinger(cls, username: str, host: str) -> dict | None:
        webfinger_url = f"https://{host}/.well-known/webfinger?resource={quote(f'acct:{username}@{host}', safe=':@')}"
        status, _headers, body, final_url = cls._fetch(webfinger_url, accept="application/jrd+json,application/json,*/*")
        if status != 200:
            return None
        data = cls._json_loads(body or "")
        if not data:
            return None
        subject = str(data.get("subject") or "").lower()
        links = data.get("links") or []
        has_actor_link = any(
            isinstance(link, dict) and "activity+json" in str(link.get("type") or "").lower()
            for link in links
        )
        if subject != f"acct:{username.lower()}@{host.lower()}" or not has_actor_link:
            return None
        result = cls._result(
            "mastodon",
            f"@{username}@{host}",
            webfinger_url,
            "mastodon_webfinger",
            status,
            final_url=final_url,
            extra={"instance": host},
        )
        result["metadata"]["url"] = f"https://{host}/@{username}"
        return result

    @classmethod
    def _probe_mastodon(cls, username: str) -> dict | None:
        handle = cls._extract_mastodon_handle(username)
        if handle:
            account, host = handle
            return cls._mastodon_webfinger(account, host)

        with ThreadPoolExecutor(max_workers=min(len(cls.MASTODON_KNOWN_HOSTS), cls.MAX_WORKERS)) as executor:
            futures = {
                executor.submit(cls._mastodon_webfinger, username, host): host
                for host in cls.MASTODON_KNOWN_HOSTS
            }
            for future in as_completed(futures):
                result = future.result()
                if result:
                    return result
        return None

    @classmethod
    def _probe_pastebin(cls, username: str) -> dict | None:
        return cls._simple_url_probe("pastebin", username, f"https://pastebin.com/u/{username}")

    @classmethod
    def _probe_reddit(cls, username: str) -> list[dict] | None:
        username = cls._clean_username(username)
        lowered = username.lower()
        requested_type = ""
        if lowered.startswith("r/"):
            requested_type = "subreddit"
            username = username.split("/", 1)[1].strip("/")
        elif lowered.startswith("u/"):
            requested_type = "user"
            username = username.split("/", 1)[1].strip("/")
        elif lowered.startswith("user/"):
            requested_type = "user"
            username = username.split("/", 1)[1].strip("/")
        if not username:
            return None

        results = []
        for account_type, url, profile_url, handle in (
            ("user", f"https://www.reddit.com/user/{username}/about.json", f"https://www.reddit.com/user/{username}/", f"user/{username}"),
            ("subreddit", f"https://www.reddit.com/r/{username}/about.json", f"https://www.reddit.com/r/{username}/", f"r/{username}"),
        ):
            if requested_type and account_type != requested_type:
                continue
            status, _headers, body, _final_url = cls._fetch(url, accept="application/json,*/*")
            if status != 200:
                continue
            data = cls._json_loads(body or "")
            if not data or data.get("error"):
                continue
            result = cls._result(
                "reddit",
                handle,
                url,
                "reddit_about_json",
                status,
                final_url=url,
                extra={"account_type": account_type},
            )
            result["metadata"]["url"] = profile_url
            results.append(result)
        if results:
            return results

        for account_type, url, profile_url, handle, required in (
            ("user", f"https://old.reddit.com/user/{username}/", f"https://www.reddit.com/user/{username}/", f"user/{username}", f"overview for {username}".lower()),
            ("subreddit", f"https://old.reddit.com/r/{username}/", f"https://www.reddit.com/r/{username}/", f"r/{username}", f"r/{username}".lower()),
        ):
            if requested_type and account_type != requested_type:
                continue
            status, _headers, body, final_url = cls._fetch(url)
            if status != 200:
                continue
            if required not in (body or "").lower() and f"/{username.lower()}/" not in (final_url or "").lower():
                continue
            result = cls._result(
                "reddit",
                handle,
                url,
                "reddit_html_profile",
                status,
                final_url=final_url,
                extra={"account_type": account_type},
            )
            result["metadata"]["url"] = profile_url
            results.append(result)
        return results or None

    @classmethod
    def _probe_tiktok(cls, username: str) -> dict | None:
        return cls._simple_url_probe(
            "tiktok",
            username,
            f"https://www.tiktok.com/@{username}",
            missing_markers=(
                "couldn't find this account",
                "couldn’t find this account",
                "couldn\\u2019t find this account",
                "couldn&#39;t find this account",
                "couldn&#x27;t find this account",
                "looking for videos? try browsing",
                "trending creators, hashtags, and sounds",
                "user doesn't exist",
                "user doesn’t exist",
                "user-not-found",
            ),
            required_any=(f"@{username}",),
        )

    @classmethod
    def _probe_twitter(cls, username: str) -> dict | None:
        return cls._simple_url_probe(
            "twitter",
            username,
            f"https://x.com/{username}",
            missing_markers=("this account doesn", "account doesn’t exist", "page doesn’t exist"),
            required_any=(f"/{username}", f"@{username}"),
        )

    @classmethod
    def _probe_whatsapp(cls, username: str) -> dict | None:
        # WhatsApp does not expose username profiles. Avoid false positives from wa.me redirect pages.
        return None

    @classmethod
    def _probe_youtube(cls, username: str) -> dict | None:
        return cls._simple_url_probe(
            "youtube",
            username,
            f"https://www.youtube.com/@{username}",
            missing_markers=("this page isn't available", "404 not found"),
            required_any=(f"@{username}",),
        )

    @classmethod
    def _probe_for_platform(cls, platform: str, username: str) -> dict | list[dict] | None:
        probe = getattr(cls, f"_probe_{platform}", None)
        if not probe:
            return None
        try:
            return probe(username)
        except Exception:
            return None

    @classmethod
    def _mastodon_result_from_url(cls, url: str) -> dict | None:
        parsed = urlparse(url)
        host = cls._host_without_www(parsed.netloc)
        username, handle, canonical_url = cls._extract_mastodon_identity_from_url(url)
        if not host or not username:
            return None
        result = cls._mastodon_webfinger(username, host)
        if result:
            result["metadata"]["url"] = canonical_url or result["metadata"]["url"]
            result["data"]["profile_existence_proof"]["input_url"] = url
            return result
        return None

    @classmethod
    def _direct_platform_parts(cls, url: str) -> tuple[str, str] | None:
        parsed = urlparse(url)
        host = cls._host_without_www(parsed.netloc)
        parts = cls._first_path_parts(url)
        if not host:
            return None

        if host in {"instagram.com"} and parts:
            return "instagram", parts[0].lstrip("@")
        if host in {"facebook.com", "fb.com"} and parts:
            return "facebook", parts[0]
        if host == "linkedin.com" and len(parts) > 1 and parts[0].lower() == "in":
            return "linkedin", parts[1]
        if host in {"x.com", "twitter.com"} and parts:
            return "twitter", parts[0]
        if host == "tiktok.com" and parts and parts[0].startswith("@"):
            return "tiktok", parts[0].lstrip("@")
        if host == "youtube.com" and parts and parts[0].startswith("@"):
            return "youtube", parts[0].lstrip("@")
        if host == "pastebin.com" and len(parts) > 1 and parts[0].lower() == "u":
            return "pastebin", parts[1]
        if host in {"reddit.com", "old.reddit.com", "new.reddit.com", "np.reddit.com"} and len(parts) > 1:
            if parts[0].lower() in {"user", "u", "r"}:
                return "reddit", parts[1]
        if host == "discord.com" and len(parts) > 1 and parts[0].lower() == "users":
            return "discord", parts[1]
        if host in {"wa.me", "api.whatsapp.com", "whatsapp.com"}:
            return "whatsapp", parts[0] if parts else ""
        if host in cls.MASTODON_KNOWN_HOSTS or (parts and (parts[0].startswith("@") or parts[0] == "users")):
            return "mastodon", url
        return None

    def parse_direct(self, value: str) -> list[dict]:
        handle = self._extract_mastodon_handle(value)
        if handle:
            account, host = handle
            result = self._mastodon_webfinger(account, host)
            return [result] if result else []

        url = self._coerce_url(value)
        if not url:
            return []

        platform_parts = self._direct_platform_parts(url)
        if not platform_parts:
            return []

        platform, username = platform_parts
        if platform == "mastodon":
            result = self._mastodon_result_from_url(url)
        else:
            result = self._probe_for_platform(platform, username)
            results = result if isinstance(result, list) else ([result] if result else [])
            for item in results:
                item["data"]["profile_existence_proof"]["input_url"] = url
            return results
        return [result] if result else []

    def parse_username(self, username: str, existing_results: list[dict] | None = None) -> list[dict]:
        username = self._clean_username(username)
        if not username or "/" in username or " " in username:
            return []

        existing_platforms = self._existing_platforms(existing_results)
        platforms = [platform for platform in self.PLATFORM_ORDER if platform == "reddit" or platform not in existing_platforms]
        if not platforms:
            return []

        results_by_platform: dict[str, list[dict]] = {}
        with ThreadPoolExecutor(max_workers=min(len(platforms), self.MAX_WORKERS)) as executor:
            futures = {
                executor.submit(self._probe_for_platform, platform, username): platform
                for platform in platforms
            }
            for future in as_completed(futures):
                platform = futures[future]
                result = future.result()
                if result:
                    results_by_platform[platform] = result if isinstance(result, list) else [result]

        return [
            item
            for platform in platforms
            for item in results_by_platform.get(platform, [])
        ]
