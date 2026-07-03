import ast
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote, unquote, urlparse
from urllib.request import Request, urlopen


class custom_recon:
    REQUEST_TIMEOUT = 4
    MAX_RESPONSE_BYTES = 32_000
    MAX_WORKERS = 16
    USER_AGENT = "Mozilla/5.0 (compatible; Orion-Social-Recon/1.0)"

    CONFIG_CACHE: dict[str, dict] | None = None

    PLATFORM_ALIASES = {
        "x": "twitter",
        "dev.to": "devto",
        "docker hub": "dockerhub",
        "internet archive": "archive_org",
        "archive of our own": "archiveofourown",
        "ao3": "archiveofourown",
        "anime planet": "anime_planet",
        "chess.com": "chess_com",
        "github sponsors": "github_sponsors",
        "hatena blog": "hatena_blog",
        "line voom": "line_voom",
        "linked in": "linkedin",
        "lnk.bio": "lnk_bio",
        "my anime list": "myanimelist",
        "myanimelist": "myanimelist",
        "naver blog": "naver_blog",
        "ok.ru": "ok_ru",
        "open collective": "opencollective",
        "product hunt": "producthunt",
        "semantic scholar": "semantic_scholar",
        "snapchat": "snapchat_public",
        "snapchat public": "snapchat_public",
        "solo.to": "solo_to",
        "stack overflow": "stackoverflow",
        "steam community": "steam_community",
        "youtube user": "youtube",
    }

    RESERVED_USERNAMES = {
        "about",
        "account",
        "admin",
        "api",
        "assets",
        "auth",
        "blog",
        "channel",
        "channels",
        "contact",
        "explore",
        "help",
        "home",
        "login",
        "logout",
        "member",
        "members",
        "people",
        "privacy",
        "profile",
        "profiles",
        "register",
        "search",
        "settings",
        "signup",
        "sponsors",
        "static",
        "support",
        "t",
        "tag",
        "tagged",
        "tags",
        "terms",
        "topic",
        "topics",
        "user",
        "users",
        "watch",
    }

    MISSING_MARKERS = (
        "404 not found",
        "page not found",
        "profile not found",
        "user not found",
        "account not found",
        "not found",
        "does not exist",
        "doesn't exist",
        "could not find",
        "couldn't find",
        "no such user",
        "this page is unavailable",
        "this page isn't available",
        "this profile is unavailable",
        "this account is unavailable",
        "this content isn't available",
        "profile unavailable",
    )

    BLOCK_MARKERS = (
        "<title>just a moment",
        "please wait for verification",
        "enable javascript and cookies to continue",
    )

    MASTODON_HOSTS = (
        "mastodon.social",
        "mstdn.social",
        "mas.to",
        "mastodon.online",
        "infosec.exchange",
    )

    NATIVE_PLATFORM_CONFIGS = {
        "facebook": {
            "name": "Facebook",
            "domains": ("facebook.com", "fb.com"),
            "profile_url": "https://www.facebook.com/{username}",
            "page_url": "https://www.facebook.com/{username}",
            "group_url": "https://www.facebook.com/groups/{username}",
            "module": "api.social_manager.scrapers.post_supported._facebook",
            "scraper_class": "_facebook",
        },
        "instagram": {
            "name": "Instagram",
            "domains": ("instagram.com",),
            "profile_url": "https://www.instagram.com/{username}/",
            "module": "api.social_manager.scrapers.post_supported._instagram",
            "scraper_class": "_instagram",
        },
        "mastodon": {
            "name": "Mastodon",
            "domains": MASTODON_HOSTS,
            "profile_url": "https://mastodon.social/@{username}",
            "url_templates": tuple(("profile", f"https://{host}/@{{username}}") for host in MASTODON_HOSTS),
            "module": "api.social_manager.scrapers.post_supported._mastodon",
            "scraper_class": "_mastodon",
        },
        "pastebin": {
            "name": "Pastebin",
            "domains": ("pastebin.com",),
            "profile_url": "https://pastebin.com/u/{username}",
            "module": "api.social_manager.scrapers.post_supported._pastebin",
            "scraper_class": "_pastebin",
        },
        "reddit": {
            "name": "Reddit",
            "domains": ("reddit.com", "old.reddit.com", "new.reddit.com", "np.reddit.com"),
            "profile_url": "https://old.reddit.com/user/{username}/",
            "url_templates": (
                ("profile", "https://old.reddit.com/user/{username}/"),
                ("profile", "https://old.reddit.com/u/{username}/"),
                ("group", "https://old.reddit.com/r/{username}/"),
                ("search", "https://old.reddit.com/search/?q={username}&type=communities"),
            ),
            "module": "api.social_manager.scrapers.post_supported._reddit",
            "scraper_class": "_reddit",
        },
        "tiktok": {
            "name": "TikTok",
            "domains": ("tiktok.com",),
            "profile_url": "https://www.tiktok.com/@{username}",
            "module": "api.social_manager.scrapers.post_supported._tiktok",
            "scraper_class": "_tiktok",
        },
        "twitter": {
            "name": "Twitter",
            "domains": ("x.com", "twitter.com"),
            "profile_url": "https://x.com/{username}",
            "url_templates": (
                ("profile", "https://x.com/{username}"),
                ("profile", "https://twitter.com/{username}"),
            ),
            "module": "api.social_manager.scrapers.post_supported._twitter",
            "scraper_class": "_twitter",
        },
        "youtube": {
            "name": "YouTube",
            "domains": ("youtube.com", "youtu.be"),
            "profile_url": "https://www.youtube.com/@{username}",
            "url_templates": (
                ("profile", "https://www.youtube.com/@{username}"),
                ("channel", "https://www.youtube.com/channel/{username}"),
                ("channel", "https://www.youtube.com/c/{username}"),
                ("user", "https://www.youtube.com/user/{username}"),
            ),
            "module": "api.social_manager.scrapers.post_supported._youtube",
            "scraper_class": "_youtube",
        },
    }

    ROUTE_PREFIXES = {
        "devto": {"t": "tag", "tag": "tag", "tags": "tag", "search": "search"},
        "facebook": {"groups": "group", "pages": "page", "watch": "video", "search": "search", "hashtag": "tag", "hashtags": "tag"},
        "habr": {"ru": "section", "en": "section", "search": "search", "users": "profile"},
        "hackernoon": {"tag": "tag", "tagged": "tag"},
        "hashnode": {"tag": "tag", "tags": "tag", "search": "search"},
        "instagram": {"explore": "explore", "p": "post", "reel": "post", "stories": "story"},
        "linkedin": {"company": "company", "showcase": "page", "in": "profile", "posts": "post"},
        "medium": {"tag": "tag", "tagged": "tag", "topic": "topic", "search": "search"},
        "nostr": {"p": "profile", "t": "tag"},
        "pastebin": {"u": "profile"},
        "primal": {"p": "profile", "search": "search"},
        "reddit": {"r": "group", "u": "profile", "user": "profile", "search": "search"},
        "stackoverflow": {"questions": "question", "tags": "tag", "users": "profile", "search": "search"},
        "substack": {"s": "post", "p": "post", "archive": "archive"},
        "threads": {"search": "search"},
        "tiktok": {"tag": "tag", "search": "search"},
        "twitter": {"hashtag": "tag", "search": "search", "i": "route"},
        "youtube": {"results": "search", "hashtag": "tag", "c": "channel", "channel": "channel", "user": "user"},
    }

    @staticmethod
    def _timestamp() -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def _normalize_platform_token(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", (value or "").strip().lower()).strip("_")

    @staticmethod
    def _compact_platform_token(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", (value or "").strip().lower())

    @classmethod
    def _platform_key(cls, value: str) -> str:
        key = (value or "").strip().lower()
        if not key:
            return ""
        key = cls.PLATFORM_ALIASES.get(key, key)
        normalized = cls.PLATFORM_ALIASES.get(cls._normalize_platform_token(key), cls._normalize_platform_token(key))
        compact = cls._compact_platform_token(key)
        configs = cls._public_platform_configs()
        if key in configs:
            return key
        if normalized in configs:
            return normalized
        for platform, config in configs.items():
            display = str(config.get("name") or "")
            if normalized == cls._normalize_platform_token(display) or compact == cls._compact_platform_token(display):
                return platform
        return normalized or key

    @classmethod
    def _platform_display_name(cls, platform: str) -> str:
        config = cls._public_platform_configs().get(platform) or {}
        return str(config.get("name") or platform.replace("_", " ").title())

    @classmethod
    def _scraper_root(cls) -> Path:
        return Path(__file__).resolve().parents[1] / "scrapers"

    @classmethod
    def _source_module(cls, path: Path) -> str:
        try:
            return ".".join(path.with_suffix("").relative_to(Path(__file__).resolve().parents[3]).parts)
        except Exception:
            return path.stem

    @classmethod
    def _iter_scraper_config_paths(cls) -> tuple[Path, ...]:
        root = cls._scraper_root()
        ordered_dirs = (root / "post_supported", root / "other", root)
        paths = []
        seen = set()
        for directory in ordered_dirs:
            if not directory.exists():
                continue
            for path in sorted(directory.glob("_*.py")):
                if path.name == "__init__.py" or path in seen:
                    continue
                paths.append(path)
                seen.add(path)
        for path in sorted(root.rglob("_*.py")):
            if "__pycache__" in path.parts or path.name == "__init__.py" or path in seen:
                continue
            paths.append(path)
            seen.add(path)
        return tuple(paths)

    @classmethod
    def _read_platform_config(cls, path: Path) -> tuple[str, dict] | None:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            raw_config = None
            for node in tree.body:
                if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                    continue
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if any(isinstance(target, ast.Name) and target.id == "PLATFORM_CONFIG" for target in targets):
                    raw_config = ast.literal_eval(node.value)
                    break
        except Exception:
            return None

        if not isinstance(raw_config, dict):
            return None
        profile_url = raw_config.get("profile_url")
        domains = raw_config.get("domains")
        if not isinstance(profile_url, str) or not isinstance(domains, list):
            return None

        platform = path.stem.lstrip("_")
        config = {
            "name": raw_config.get("name") if isinstance(raw_config.get("name"), str) else platform.replace("_", " ").title(),
            "domains": tuple(str(domain).lower() for domain in domains if domain),
            "profile_url": profile_url,
            "module": cls._source_module(path),
            "scraper_class": f"_{platform}",
            "source_path": str(path),
        }
        for key in ("page_url", "group_url", "posts_url"):
            if isinstance(raw_config.get(key), str):
                config[key] = raw_config[key]
        if isinstance(raw_config.get("subdomain"), bool):
            config["subdomain"] = raw_config["subdomain"]
        return platform, config

    @classmethod
    def _public_platform_configs(cls) -> dict[str, dict]:
        if cls.CONFIG_CACHE is not None:
            return cls.CONFIG_CACHE

        configs = {platform: dict(config) for platform, config in cls.NATIVE_PLATFORM_CONFIGS.items()}
        for path in cls._iter_scraper_config_paths():
            item = cls._read_platform_config(path)
            if not item:
                continue
            platform, config = item
            configs[platform] = config
        cls.CONFIG_CACHE = configs
        return configs

    @classmethod
    def _platform_order(cls) -> tuple[str, ...]:
        return tuple(cls._public_platform_configs().keys())

    @classmethod
    def _existing_platforms(cls, existing_results: list[dict] | None) -> set[str]:
        out = set()
        for item in existing_results or []:
            platform = cls._platform_key(((item or {}).get("metadata") or {}).get("platform") or "")
            if platform:
                out.add(platform)
        return out

    @staticmethod
    def _host_without_www(host: str) -> str:
        host = (host or "").lower().split(":")[0]
        return host[4:] if host.startswith("www.") else host

    @classmethod
    def _host_matches_domain(cls, host: str, domain: str) -> bool:
        clean_host = cls._host_without_www(host)
        clean_domain = cls._host_without_www(domain)
        return clean_host == clean_domain or clean_host.endswith(f".{clean_domain}")

    @classmethod
    def _coerce_url(cls, value: str) -> str | None:
        v = (value or "").strip()
        if re.match(r"^https?://", v, flags=re.IGNORECASE):
            return v
        if re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$", v):
            return f"https://{v}"
        return None

    @staticmethod
    def _url_component_parts(value: str) -> list[str]:
        return [unquote(part) for part in (value or "").split("/") if part]

    @classmethod
    def _first_path_parts(cls, url: str) -> list[str]:
        return cls._url_component_parts(urlparse(url).path)

    @staticmethod
    def _clean_username(username: str) -> str:
        return (username or "").strip().strip("/").lstrip("@~")

    @classmethod
    def _valid_identity(cls, value: str, allow_reserved: bool = False, allow_spaces: bool = False) -> bool:
        clean = cls._clean_username(value)
        if not clean or len(clean) > 160:
            return False
        if not allow_spaces and any(char.isspace() for char in clean):
            return False
        if not allow_reserved and clean.lower() in cls.RESERVED_USERNAMES:
            return False
        return True

    @staticmethod
    def _extract_template_token_value(template_part: str, actual_part: str, token: str) -> str | None:
        if token not in template_part:
            return None
        prefix, suffix = template_part.split(token, 1)
        if prefix and not actual_part.startswith(prefix):
            return None
        if suffix and not actual_part.endswith(suffix):
            return None
        end = len(actual_part) - len(suffix) if suffix else len(actual_part)
        return actual_part[len(prefix):end].strip().strip("/").lstrip("@~") or None

    @classmethod
    def _match_template_parts(cls, template_parts: list[str], actual_parts: list[str], token: str) -> str | None:
        if not template_parts:
            return None
        if len(actual_parts) < len(template_parts):
            return None
        candidate = None
        for index, template_part in enumerate(template_parts):
            actual_part = actual_parts[index]
            if token in template_part:
                candidate = cls._extract_template_token_value(template_part, actual_part, token)
                if not candidate:
                    return None
                continue
            if template_part.lower() != actual_part.lower():
                return None
        return candidate

    @staticmethod
    def _static_template_parts_match(template_parts: list[str], actual_parts: list[str]) -> bool:
        if len(actual_parts) < len(template_parts):
            return False
        return all(template_part.lower() == actual_parts[index].lower() for index, template_part in enumerate(template_parts))

    @classmethod
    def _extract_username_from_template(cls, template: str, url: str) -> str | None:
        token = "__ORION_USERNAME__"
        template_url = template.replace("{username}", token)
        parsed_template = urlparse(template_url)
        parsed_url = urlparse(url)
        template_host = cls._host_without_www(parsed_template.netloc)
        actual_host = cls._host_without_www(parsed_url.netloc)
        token_lower = token.lower()
        candidate = None

        if token_lower in template_host:
            pattern = re.escape(template_host).replace(re.escape(token_lower), r"(?P<username>[^.]+)")
            match = re.fullmatch(pattern, actual_host)
            if not match:
                return None
            candidate = match.group("username").strip().lstrip("@~") or None
        elif template_host and not cls._host_matches_domain(actual_host, template_host):
            return None

        template_parts = cls._url_component_parts(parsed_template.path)
        actual_parts = cls._url_component_parts(parsed_url.path)
        if any(token in part for part in template_parts):
            candidate = cls._match_template_parts(template_parts, actual_parts, token)
            if not candidate:
                return None
        elif template_parts and not cls._static_template_parts_match(template_parts, actual_parts):
            return None

        template_query = parse_qsl(parsed_template.query, keep_blank_values=True)
        actual_query = dict(parse_qsl(parsed_url.query, keep_blank_values=True))
        for key, template_value in template_query:
            if token not in template_value:
                continue
            if key not in actual_query:
                return None
            candidate = cls._extract_template_token_value(template_value, actual_query[key], token)
            if not candidate:
                return None

        template_fragment_parts = cls._url_component_parts(parsed_template.fragment)
        actual_fragment_parts = cls._url_component_parts(parsed_url.fragment)
        if any(token in part for part in template_fragment_parts):
            candidate = cls._match_template_parts(template_fragment_parts, actual_fragment_parts, token)
            if not candidate:
                return None
        elif template_fragment_parts and not cls._static_template_parts_match(template_fragment_parts, actual_fragment_parts):
            return None

        return candidate

    @classmethod
    def _template_items(cls, config: dict, include_posts: bool = True) -> tuple[tuple[str, str], ...]:
        items = []
        seen = set()
        keys = (("profile", "profile_url"), ("page", "page_url"), ("group", "group_url"))
        if include_posts:
            keys = (*keys, ("posts", "posts_url"))
        for target_type, key in keys:
            value = config.get(key)
            values = value if isinstance(value, (list, tuple)) else (value,)
            for template in values:
                if isinstance(template, str) and "{username}" in template and template not in seen:
                    items.append((target_type, template))
                    seen.add(template)
        for item in config.get("url_templates") or ():
            if isinstance(item, dict):
                target_type = str(item.get("target_type") or item.get("type") or "profile")
                template = item.get("template") or item.get("url")
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                target_type, template = str(item[0]), item[1]
            else:
                continue
            if isinstance(template, str) and "{username}" in template and template not in seen:
                items.append((target_type, template))
                seen.add(template)
        return tuple(items)

    @classmethod
    def _format_template(cls, template: str, username: str) -> str:
        return template.format(username=quote(username, safe=""))

    @classmethod
    def _candidate_from_template(cls, platform: str, config: dict, url: str, include_posts: bool = True) -> dict | None:
        for target_type, template in cls._template_items(config, include_posts=include_posts):
            username = cls._clean_username(cls._extract_username_from_template(template, url) or "")
            if not cls._valid_identity(username):
                continue
            return cls._candidate(platform, username, url, target_type, "template", config)
        return None

    @classmethod
    def _platform_for_host(cls, host: str) -> tuple[str, dict] | tuple[None, None]:
        for platform, config in cls._public_platform_configs().items():
            if any(cls._host_matches_domain(host, domain) for domain in config.get("domains") or ()):
                return platform, config
        return None, None

    @classmethod
    def _query_value(cls, url: str, *keys: str) -> str:
        query = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        for key in keys:
            value = (query.get(key) or "").strip()
            if value:
                return value
        return ""

    @classmethod
    def _route_identity(cls, platform: str, url: str) -> tuple[str, str] | tuple[None, None]:
        parsed = urlparse(url)
        path = cls._first_path_parts(url)
        fragment = cls._url_component_parts(parsed.fragment)
        parts = fragment if platform in {"nostr"} and fragment else path
        if not parts:
            query_label = cls._query_value(url, "q", "query", "search_query")
            return (query_label, "search") if query_label else (None, None)

        first = parts[0].lower()
        second = parts[1] if len(parts) > 1 else ""
        third = parts[2] if len(parts) > 2 else ""
        query_label = cls._query_value(url, "q", "query", "search_query")

        if platform == "devto" and first in {"t", "tag", "tags"}:
            return second, "tag"
        if platform == "hashnode" and first in {"tag", "tags"}:
            return second, "tag"
        if platform == "medium" and first in {"tag", "tagged"}:
            return second, "tag"
        if platform == "medium" and first == "topic":
            return second, "topic"
        if platform == "hackernoon" and first in {"tag", "tagged"}:
            return second, "tag"
        if platform == "habr":
            if first in {"ru", "en"} and second.lower() in {"hub", "hubs"}:
                return third, "hub"
            if first in {"ru", "en"} and second.lower() == "users":
                return third, "profile"
        if platform == "stackoverflow":
            if first == "questions" and second.lower() == "tagged":
                return third, "tag"
            if first == "questions" and second.isdigit():
                return second, "question"
        if platform == "instagram":
            if first == "explore" and second.lower() == "tags":
                return third, "tag"
            if first == "explore" and second.lower() == "locations":
                return third, "location"
        if platform == "linkedin":
            if first in {"company", "showcase", "in", "posts"}:
                return second, cls.ROUTE_PREFIXES.get(platform, {}).get(first) or "route"
        if platform == "facebook":
            if first == "pages":
                return (parts[-1] if len(parts) > 2 else second), "page"
            if first == "watch":
                return cls._query_value(url, "v") or second, "video"
        if platform == "reddit" and first == "r" and len(parts) > 2 and parts[2].lower() == "search":
            return query_label, "search"
        if platform == "twitter" and first == "i":
            if second.lower() == "lists":
                return third, "list"
            return None, None
        if platform == "youtube" and first == "results":
            return query_label, "search"
        if platform == "primal" and first == "search":
            return unquote(second).lstrip("#"), "search"

        route_type = cls.ROUTE_PREFIXES.get(platform, {}).get(first)
        if route_type == "search":
            return query_label or second, route_type
        if route_type:
            return second, route_type
        return None, None

    @classmethod
    def _candidate(cls, platform: str, username: str, url: str, target_type: str, source: str, config: dict) -> dict:
        return {
            "platform": platform,
            "platform_name": cls._platform_display_name(platform),
            "username": cls._clean_username(username),
            "target_type": target_type,
            "url": url,
            "source": source,
            "module": config.get("module"),
            "scraper_class": config.get("scraper_class"),
            "source_path": config.get("source_path"),
        }

    @classmethod
    def resolve_url(cls, value: str) -> dict | None:
        url = cls._coerce_url(value)
        if not url:
            return None

        for platform, config in cls._public_platform_configs().items():
            candidate = cls._candidate_from_template(platform, config, url, include_posts=True)
            if candidate:
                return candidate

        parsed = urlparse(url)
        host = cls._host_without_www(parsed.netloc)
        platform, config = cls._platform_for_host(host)
        if not platform or not config:
            return None

        label, target_type = cls._route_identity(platform, url)
        label = cls._clean_username(label or "")
        if not cls._valid_identity(label, allow_reserved=target_type in {"search", "route"}, allow_spaces=target_type == "search"):
            return None
        return cls._candidate(platform, label, url, target_type, "route", config)

    @classmethod
    def script_target(cls, platform: str, username: str, target_type: str | None = None) -> dict | None:
        platform = cls._platform_key(platform)
        config = cls._public_platform_configs().get(platform)
        username = cls._clean_username(username)
        if not config or not cls._valid_identity(username):
            return None
        target = (target_type or "profile").strip().lower()
        template_key = f"{target}_url" if target in {"page", "group"} and config.get(f"{target}_url") else "profile_url"
        url = cls._format_template(str(config[template_key]), username)
        return cls._candidate(platform, username, url, target, "script_target", config)

    @classmethod
    def _fetch(cls, url: str) -> tuple[int, dict, str, str]:
        request = Request(
            url,
            headers={
                "Accept": "text/html,application/json,*/*",
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

    @classmethod
    def _body_has_bad_marker(cls, body: str) -> bool:
        body_lower = (body or "").lower()
        return any(marker in body_lower for marker in (*cls.MISSING_MARKERS, *cls.BLOCK_MARKERS))

    @classmethod
    def _candidate_domains(cls, candidate: dict) -> tuple[str, ...]:
        config = cls._public_platform_configs().get(candidate.get("platform") or "") or {}
        return tuple(str(domain) for domain in config.get("domains") or ())

    @classmethod
    def _validate_candidate(cls, candidate: dict) -> dict | None:
        status, _headers, body, final_url = cls._fetch(candidate["url"])
        if status < 200 or status >= 400:
            return None
        final_host = cls._host_without_www(urlparse(final_url or candidate["url"]).netloc)
        domains = cls._candidate_domains(candidate)
        if domains and not any(cls._host_matches_domain(final_host, domain) for domain in domains):
            return None
        if cls._body_has_bad_marker(body):
            return None

        username = candidate["username"]
        final_lower = (final_url or "").lower()
        body_lower = (body or "").lower()
        markers = {username.lower(), quote(username, safe="").lower()}
        if not any(marker and (marker in final_lower or marker in body_lower) for marker in markers):
            return None

        validated = dict(candidate)
        validated["status_code"] = status
        validated["final_url"] = final_url or candidate["url"]
        return validated

    @classmethod
    def _result(cls, candidate: dict, proof_type: str) -> dict:
        target_type = candidate.get("target_type") or "profile"
        username = candidate.get("username") or ""
        return {
            "metadata": {
                "platform": candidate.get("platform_name") or cls._platform_display_name(candidate.get("platform") or ""),
                "platform_key": candidate.get("platform"),
                "username": username,
                "social_handle": f"{target_type}:{username}" if target_type not in {"profile", "url"} else username,
                "url": candidate.get("final_url") or candidate.get("url"),
                "timestamp": cls._timestamp(),
                "status": "active",
                "target_type": target_type,
            },
            "data": {
                "profile_existence_proof": {
                    "type": proof_type,
                    "status_code": candidate.get("status_code"),
                    "checked_url": candidate.get("url"),
                    "final_url": candidate.get("final_url") or candidate.get("url"),
                    "target_type": target_type,
                    "resolver_source": candidate.get("source"),
                    "scraper_module": candidate.get("module"),
                    "scraper_class": candidate.get("scraper_class"),
                }
            },
        }

    def parse_direct(self, value: str) -> list[dict]:
        candidate = self.resolve_url(value)
        if not candidate:
            return []
        validated = self._validate_candidate(candidate)
        return [self._result(validated, "known_scraper_direct_url")] if validated else []

    def parse_username(self, username: str, existing_results: list[dict] | None = None) -> list[dict]:
        username = self._clean_username(username)
        if not self._valid_identity(username) or "/" in username:
            return []

        existing_platforms = self._existing_platforms(existing_results)
        candidates = []
        seen_urls = set()
        for platform in self._platform_order():
            if platform in existing_platforms:
                continue
            config = self._public_platform_configs().get(platform) or {}
            for target_type, template in self._template_items(config, include_posts=False):
                if target_type not in {"profile", "page", "group", "channel", "user"}:
                    continue
                url = self._format_template(template, username)
                if (platform, url) in seen_urls:
                    continue
                seen_urls.add((platform, url))
                candidates.append(self._candidate(platform, username, url, target_type, "script_target", config))

        results_by_platform = {}
        with ThreadPoolExecutor(max_workers=min(len(candidates) or 1, self.MAX_WORKERS)) as executor:
            futures = {executor.submit(self._validate_candidate, candidate): candidate for candidate in candidates}
            for future in as_completed(futures):
                candidate = futures[future]
                if candidate["platform"] in results_by_platform:
                    continue
                try:
                    validated = future.result()
                except Exception:
                    validated = None
                if validated:
                    results_by_platform[candidate["platform"]] = self._result(validated, "known_scraper_fast_profile")

        return [results_by_platform[platform] for platform in self._platform_order() if platform in results_by_platform]
