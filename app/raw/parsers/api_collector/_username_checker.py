import re
import subprocess
from typing import Dict, List
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model


class _username_checker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_username_checker, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self._card_data: List[dict] = []
        self._entity_data: List[entity_model] = []

    @property
    def developer_signature(self) -> str:
        return "Muhammad Hassan Arshad: owEBeAKH/ZANAwAKAbKjqaChU0IoAcsxYgBoei5jVmVyaWZpZWQgZGV2ZWxvcGVyOiBNdWhhbW1hZCBIYXNzYW4gQXJzaGFkCokCMwQAAQoAHRYhBD5p3c9aqX5fJ9SIZbKjqaChU0IoBQJoei5jAAoJELKjqaChU0Io2i8QAKRGGxAbMJGV97ym5wcir4mn2es2/npd+MFDa/LZFnkcoPOP9/fKtg9pZ1a2PVa0h9s5ewU6wGJ4HIvjP/2gxd1maDIjv6IM+5mtlpJvQJhzoqHdAg//IRwJU5QO2krqxBQrtcvNwfkW1IoNSEaJCr0EmXht3rkGhkJ3J3XqEvrBeH0DtaZLnCLOJ3eTIRleqbBOUdq2Uf9hDZZY9rdqynjjsADo1lhchdyPjwBz1g8M/q1Ud3sTUA+/8gas5l15jR9SGQZxbgnzZRjG19oq5GAhLwUYgKuoH+zANQEB7leF9jBudzYz2Ey/4BglnVE6kszUo7RxPoqtNOFvq6WzCcRKPLO323sLfFYtwXDwvJ0iviVTOwrbXlA80GFANcAbSR76nN0XrsaLM2L/KT6oe0wTVq35j1QZnt4Jq5PWALA8hQNr7w1KtuwnpN5PmE741h+9OfZP2ogd9ERbmGb10DROsd9t4RL4hpxpsCoekHRbLI3XmHFZqFAB/GgF194Tmh3LcoIAcwOYty/PVDuPYMGMmm5Nttg2vvVrMg82P0LeOrIN2Mq03HCiZm/HaOvePniPg+EeaWPMiVmGWvCJUOMI/TJRz4jVLR4BUlvoiUSNBWrJhxMRQZpViam2rVUaojPaZhzoIF4sqS6hYqzZbbXHwtYjJfNOHh00gucABJHw=gmDH"

    @property
    def base_url(self) -> str:
        return "about:blank"

    @property
    def cards_data(self) -> List[dict]:
        return self._card_data

    @property
    def card_data(self) -> List[dict]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def model_dump(self) -> Dict[str, List[dict]]:
        return {"cards_data": self._card_data}

    def _check_profile(self, username: str) -> List[dict]:
        cmd = [
            "sherlock",
            username,
            "--timeout",
            "15",
            "--print-found",
            "--no-color",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
        except Exception:
            return []

        profiles: List[dict] = []
        seen = set()

        for line in (result.stdout or "").splitlines():
            line = line.strip()
            if not line.startswith("[+]"):
                continue

            match = re.search(r"https?://\S+", line)
            if not match:
                continue

            url = match.group(0).rstrip("/")
            key = url.lower()
            if key in seen:
                continue
            seen.add(key)

            domain = url.split("/")[2].replace("www.", "")
            platform = domain.split(".")[0].capitalize()

            profiles.append({"platform": platform, "url": url, "status": "active"})

        return profiles

    async def parse_leak_data(self, query: Dict[str, str], _=None):
        username = (query or {}).get("username")
        self._card_data = []

        if not username:
            return self

        profiles = self._check_profile(username)

        for p in profiles:
            url = p["url"]
            base_url = "/".join(url.split("/", 3)[:3])

            self._card_data.append(
                {
                    "m_title": f"User {username} found on {base_url}",
                    "m_url": url,
                    "m_base_url": base_url,
                    "m_content": "",
                    "m_important_content": f"Found on: {url}",
                    "m_network": "clearnet",
                    "m_section": [],
                    "m_content_type": ["stolen"],
                    "m_screenshot": "",
                    "m_weblink": [url],
                    "m_websites": [],
                    "m_logo_or_images": [],
                    "m_leak_date": None,
                    "m_data_size": None,
                    "m_revenue": None,
                }
            )

            self._entity_data.append(
                entity_model(
                    m_name=username,
                    m_username=[username],
                    m_platform=[p["platform"]],
                    m_social_media_profiles=[url],
                    m_weblink=[url],
                )
            )

        return self
