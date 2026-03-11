import re
from datetime import datetime
from abc import ABC
from typing import List, Dict
from difflib import SequenceMatcher
from urllib.parse import urljoin, quote_plus

from playwright.sync_api import BrowserContext
import requests
from crawler.crawler_instance.local_interface_model.api.api_apk_model import apk_data_model
from crawler.crawler_instance.local_interface_model.api.api_collector_interface import api_collector_interface
from crawler.crawler_instance.local_shared_model.data_model.apk_model import apk_model
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType


class _pcgame_mod(api_collector_interface, ABC):
    _instance = None

    def __init__(self):
        self._card_data: List[apk_model] = []
        self._entity_data: List[entity_model] = []
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/100 Safari/537.36"
        })

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_pcgame_mod, cls).__new__(cls)
        return cls._instance

    @property
    def developer_signature(self) -> str:
        return "Muhammad Abdullah:owGbwMvMwMEYdOzLoajv79gZTxskMWRU6bi8370 / LLUoMy0zNUUhJbUsNSe / ILXISsG3NCMxNzcxRcExKaU0Jycxg5erYzMLAyMHg6yYIkuQ4M9 / l7siYpT2b / oFM5GVCWQcAxenAEykRYSFYcHRJWUetXMKmo78Ec5ueHZq52rX / vuHpJTf / G31ULsywdC23 + fM4tmaUbP2cXYm7y9kPHnAdbXgspWerkeXW8ZYmm2xrpdTF / Yyvi0aGdn5iMne8PQGgSgWxeOMKUo8IQvL3W1PN4gtYYkxfr6kMZ3t0tmSRR2qnu / fZ2yfqfdm9szOQpt2AA ===weDX"

    @property
    def base_url(self) -> str:
        return "https://www.example.com/"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(m_fetch_proxy=FetchProxy.TOR, m_resoource_block=True, m_javascript=False,m_fetch_config=FetchConfig.REQUESTS, m_threat_type=ThreatType.API)

    @property
    def card_data(self) -> List[apk_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def append_apk_data(self, apk: apk_model):
        self._card_data.append(apk)

    PC_GAME_SITES = [
        {
            "name": "fitgirl-repacks",
            "base_url": "https://fitgirl-repacks.site",
            "search": "https://fitgirl-repacks.site/?s={game}",
            "result_pattern": r'<a[^>]+class=["\']entry-title[^"\']*["\'][^>]*href=["\'](?P<href>[^"\']+)["\'][^>]*>\s*(?P<title>[^<]{5,200})\s*</a>',
            "download_pattern_list": [
            r'href=["\'](?P<h>[^"\']*(?:torrent|magnet|mega|zippyshare|1fichier|mediafire|google|drive)[^"\']*)["\']'
            ],

            "date_pattern": r'([A-Za-z]{3,9} \d{1,2}, \d{4})'
        },
        {
            "name": "skidrowrepacks",
            "base_url": "https://skidrowrepacks.com",
            "search": "https://skidrowrepacks.com/?s={game}",
            "result_pattern": r'<h2[^>]*class=["\']entry-title["\'][^>]*>\s*<a[^>]+href=["\'](?P<href>[^"\']+)["\'][^>]*>\s*(?P<title>[^<]+)\s*</a>',
            "download_pattern_list": [
                r'href=["\'](?P<h>[^"\']*download[^"\']*)["\']',
                r'href=["\'](?P<h>[^"\']*repacks[^"\']*)["\']'
            ],
            "date_pattern": r'([A-Za-z]{3,9} \d{1,2}, \d{4})'
        },


        {
            "name": "oceantogames",
            "base_url": "https://oceantogames.com",
            "search": "https://oceantogames.com/?s={game}",
            "result_pattern": r'<a[^>]+href=["\'](?P<href>[^"\']+)["\'][^>]*>\s*(?P<title>[^<]{5,200})\s*</a>',
            "download_pattern_list": [r'href=["\'](?P<h>[^"\']*download[^"\']*)["\']',
                                      r'href=["\'](?P<h>[^"\']*drive[^"\']*)["\']'],
            "date_pattern": r'([A-Za-z]{3,9} \d{1,2}, \d{4})'
        },

        """{
            "name": "romulation",
            "base_url": "https://www.romulation.org/rom/NDS/",
            "search": "https://www.romulation.org/rom/NDS/{game}",
            "result_pattern": r'<h1[^>]*class=["\']page-title["\'][^>]*>(?P<title>[^<]+)</h1>.*?<a[^>]+href=["\'](?P<href>[^"\']+\.zip|[^"\']+\.7z)["\']',
            "download_pattern_list": [
                r'href=["\'](?P<h>https://www\.romulation\.org/rom/[^"\']+\.zip)["\']',
                r'href=["\'](?P<h>https://www\.romulation\.org/rom/[^"\']+\.7z)["\']'
            ],
            "date_pattern": r'(\d{4}-\d{2}-\d{2})'
        },

        {
            "name": "vimm",
            "base_url": "https://vimm.net",
            "search": "https://vimm.net/vault/?p=list&system={system}&q={game}",
            "result_pattern": r'<a[^>]+href=["\'](?P<href>[^"\']+)["\'][^>]*>\s*(?P<title>[^<]{5,200})\s*</a>',
            "download_pattern_list": [
                r'href=["\'](?P<h>https://vimm\.net/download/[^"\']+)["\']',
                r'href=["\'](?P<h>https://vimm\.net/files/[^"\']+)["\']'
            ],
            "date_pattern": r'(\d{4}-\d{2}-\d{2})'
        }"""
    ]

    @staticmethod
    def similarity(a: str, b: str) -> float:
        def clean(text: str) -> str:
            text = (text or "").lower()
            text = re.sub(r"\b\d+(\.\d+)*\b", "", text)
            text = re.sub(r"[^a-z0-9\s]", "", text)
            return text.strip()

        a_clean = clean(a)
        b_clean = clean(b)

        if a_clean == b_clean:
            return 1.0
        if a_clean and a_clean in b_clean:
            return 0.95

        return SequenceMatcher(None, a_clean, b_clean).ratio()

    def _get_text(self, url: str, timeout: int = 20) -> str:
        try:
            resp = self._session.get(url, timeout=timeout, allow_redirects=True)
            resp.encoding = resp.apparent_encoding or resp.encoding
            return resp.text or ""
        except Exception as e:
            return ""

    def search_site(self, site: Dict, game_name: str) -> List[tuple]:

        search_url = site["search"].format(game=quote_plus(game_name))
        html = self._get_text(search_url)

        pattern = re.compile(site.get("result_pattern", r'<a[^>]+href=["\'](?P<href>[^"\']+)["\'][^>]*>(?P<title>[^<]+)</a>'),
                             flags=re.IGNORECASE | re.DOTALL)
        matches = pattern.finditer(html)

        collected = []
        seen = set()
        for m in matches:
            href = m.groupdict().get("href", "").strip()
            title = m.groupdict().get("title", "").strip()
            if not href or not title:
                continue

            if href.startswith("/"):
                href = urljoin(site["base_url"], href)
            if href in seen:
                continue
            seen.add(href)
            collected.append((title, href))
            if len(collected) >= 10:
                break

        if not collected:
            generic_pattern = re.compile(r'<a[^>]+href=["\'](?P<href>[^"\']+)["\'][^>]*>\s*(?P<title>[^<]{5,200})\s*</a>',
                                         flags=re.IGNORECASE | re.DOTALL)
            for m in generic_pattern.finditer(html):
                href = m.group("href").strip()
                title = m.group("title").strip()
                if href.startswith("/"):
                    href = urljoin(site["base_url"], href)
                if href in seen:
                    continue
                if self.similarity(game_name, title) > 0.35:
                    seen.add(href)
                    collected.append((title, href))
                if len(collected) >= 10:
                    break

        return collected[:5]

    @staticmethod
    def parse_date(date_str: str) -> str | None:
        if not date_str:
            return None

        match = re.search(r"([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})", date_str)
        if match:
            date_text = match.group(1)
            for fmt in ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%Y-%m-%d"):
                try:
                    dt = datetime.strptime(date_text, fmt)
                    return dt.strftime("%Y-%m-%d")
                except Exception:
                    continue

        match = re.search(r"(\d{4}-\d{2}-\d{2})", date_str)
        if match:
            return match.group(1)
        return None

    def extract_metadata(self, site: Dict, href: str) -> Dict:
        full_url = href if href.startswith("http") else urljoin(site["base_url"], href)
        html = self._get_text(full_url)
        meta: Dict = {"url": full_url}


        title = None
        m = re.search(r'<h1[^>]*>(?P<t>[^<]{2,300})</h1>', html, flags=re.IGNORECASE | re.DOTALL)
        if m:
            title = re.sub(r"\s+", " ", m.group("t")).strip()

        if not title:
            m = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](?P<t>[^"\']+)["\']', html,
                          flags=re.IGNORECASE)
            if m:
                title = m.group("t").strip()

        if not title:
            m = re.search(r'<title[^>]*>(?P<t>[^<]+)</title>', html, flags=re.IGNORECASE | re.DOTALL)
            if m:
                title = m.group("t").split("|")[0].strip()

        meta["details_title"] = title or ""

        downloads = []
        for dp in site.get("download_pattern_list", []):
            for m in re.finditer(dp, html, flags=re.IGNORECASE):
                h = m.groupdict().get("h") or m.group(1)
                if not h:
                    continue
                if h.startswith("/") and not h.startswith("//"):
                    h = urljoin(site["base_url"], h)
                if h.startswith("//"):
                    h = "https:" + h
                if not h.startswith("http"):
                    h = urljoin(full_url, h)
                if h not in downloads:
                    downloads.append(h)

        if not downloads:
            for m in re.finditer(r'href=["\'](?P<h>[^"\']+)["\'][^>]*>(?P<txt>[^<]{0,200})</a>',
                                 html, flags=re.IGNORECASE | re.DOTALL):
                h = m.group("h").strip()
                txt = m.group("txt").lower()

                if any(k in txt for k in (
                        "download", "torrent", "mega", "drive", "google", "dl", "repacks", "file"
                )) or any(k in h.lower() for k in (
                        "download", "torrent", "mega", "drive", "google", "dl", "repacks"
                )):
                    if h.startswith("/") and not h.startswith("//"):
                        h = urljoin(site["base_url"], h)
                    if h.startswith("//"):
                        h = "https:" + h
                    if not h.startswith("http"):
                        h = urljoin(full_url, h)
                    if h not in downloads:
                        downloads.append(h)

        meta["download"] = downloads

        magnets = re.findall(r'href=["\'](magnet:\?xt=[^"\']+)["\']', html, flags=re.IGNORECASE)
        meta["magnet_links"] = list(set(magnets))

        mpass = re.search(r'(password|pwd)[:\s]*([A-Za-z0-9\-\._]+)', html, flags=re.IGNORECASE)
        meta["password"] = mpass.group(2) if mpass else ""


        mver = re.search(r'Version[:\s]*([^<\n]{2,80})', html, flags=re.IGNORECASE)
        meta["version"] = mver.group(1).strip() if mver else ""


        msize = re.search(r'(Size|File size)[:\s]*([^<\n]{2,80})', html, flags=re.IGNORECASE)
        meta["size"] = msize.group(2).strip() if msize else ""

        mgenre = re.search(r'(Genre|Categories?)[:\s]*([^<\n]{2,80})', html, flags=re.IGNORECASE)
        meta["genre"] = mgenre.group(2).strip() if mgenre else ""

        mplat = re.search(r'(Platform|System|OS)[:\s]*([^<\n]{2,80})', html, flags=re.IGNORECASE)
        meta["platform"] = mplat.group(2).strip() if mplat else "PC"


        mdev = re.search(r'(Developer|Studio)[:\s]*([^<\n]{2,80})', html, flags=re.IGNORECASE)
        meta["developer"] = mdev.group(2).strip() if mdev else ""

        mpub = re.search(r'(Publisher)[:\s]*([^<\n]{2,80})', html, flags=re.IGNORECASE)
        meta["publisher"] = mpub.group(2).strip() if mpub else ""

        mrel = re.search(r'(Release Date|Released|Date)[:\s]*([^<\n]{2,80})', html, flags=re.IGNORECASE)
        meta["release_date"] = self.parse_date(mrel.group(2)) if mrel else ""


        date_found = None
        dp = site.get("date_pattern")
        if dp:
            mdate = re.search(dp, html, flags=re.IGNORECASE)
            if mdate:
                date_found = self.parse_date(mdate.group(1))

        if not date_found:
            mdate = re.search(r'(\d{4}-\d{2}-\d{2})', html)
            if mdate:
                date_found = mdate.group(1)

        meta["last_update"] = date_found


        desc = ""
        md = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']', html,
                       flags=re.IGNORECASE)
        if md:
            desc = md.group(1)

        if not desc:
            md2 = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html,
                            flags=re.IGNORECASE)
            if md2:
                desc = md2.group(1)

        if not desc:
            mp = re.search(r'<p[^>]*>([^<]{30,500})</p>', html, flags=re.IGNORECASE)
            if mp:
                desc = mp.group(1).strip()

        meta["description"] = desc


        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, flags=re.IGNORECASE)
        clean_imgs = []
        for img in imgs:
            img = img.strip()
            if img.startswith("//"): img = "https:" + img
            if img.startswith("/") and not img.startswith("//"):
                img = urljoin(site["base_url"], img)
            if img.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                clean_imgs.append(img)
        meta["screenshots"] = list(set(clean_imgs))[:10]


        sysreq = re.findall(r'(Minimum|Recommended)[^<]{5,400}', html, flags=re.IGNORECASE)
        meta["system_requirements"] = sysreq


        meta["pkg_id"] = re.sub(r'[^a-zA-Z0-9\-_\.]', '-', full_url)

        return meta


    async def parse_leak_data(self, query: Dict, context: BrowserContext):
        name = query.get("name")

        if not isinstance(query, dict):
            return None

        if name:
            game_name = name.strip()
        else:
            return None

        all_best_results = []

        for site in self.PC_GAME_SITES:
            try:
                collected = self.search_site(site, game_name)

                best_site_result = None
                best_site_score = 0.0

                for title, href in collected:
                    score = self.similarity(game_name, title)
                    if score > best_site_score:
                        best_site_score = score
                        best_site_result = (site, title, href, score)

                if best_site_result:
                    all_best_results.append(best_site_result)

            except Exception as e:
                pass

        found_cards: List[apk_model] = []
        found_entities: List[entity_model] = []

        for site, title, href, score in all_best_results:
            try:
                meta = self.extract_metadata(site, href)
            except Exception as e:
                continue

            card_data = apk_model(
                m_app_name=meta.get("details_title") or title,
                m_app_url=meta.get("url") or href,
                m_package_id=meta.get("pkg_id") or "",
                m_mod_features="",
                m_network="clearnet",
                m_version=meta.get("version") or "",
                m_content_type=["pc_game"],
                m_latest_date=str(meta.get("last_update") or "")
            )
            if card_data.m_app_name.__contains__("contact") or card_data.m_app_name.__contains__("Archive"):
                continue

            found_cards.append(card_data)
            self.append_apk_data(card_data)

        self._card_data.extend(found_cards)
        self._entity_data.extend(found_entities)

        model = apk_data_model(base_url=self.base_url, content_type=["pc_game"])
        model.cards_data = self.card_data
        return model