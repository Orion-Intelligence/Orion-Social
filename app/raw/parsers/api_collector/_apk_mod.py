import re

from datetime import datetime
from abc import ABC
from typing import List, Dict
from difflib import SequenceMatcher
from urllib.parse import urljoin
from playwright.async_api import BrowserContext

from crawler.crawler_instance.local_interface_model.api.api_apk_model import apk_data_model
from crawler.crawler_instance.local_interface_model.api.api_collector_interface import api_collector_interface
from crawler.crawler_instance.local_shared_model.data_model.apk_model import apk_model
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType

class _apk_mod(api_collector_interface, ABC):
    _instance = None

    def __init__(self):
        self._card_data = []
        self._entity_data = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_apk_mod, cls).__new__(cls)
        return cls._instance

    @property
    def developer_signature(self) -> str:
        return "Muhammad Marij Younas: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9UyN"

    @property
    def base_url(self) -> str:
        return "https://www.example.com/"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(m_fetch_proxy=FetchProxy.NONE, m_resoource_block=True, m_javascript=False,m_fetch_config=FetchConfig.PLAYRIGHT, m_threat_type=ThreatType.API)

    @property
    def card_data(self) -> List[apk_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def append_apk_data(self, apk: apk_model):
        self._card_data.append(apk)

    APK_SITES = [
        {
            "name": "9mod",
            "base_url": "https://9mod.com",
            "search": "https://9mod.com/?s={apk_name}",
            "selectors": {
                "results": "a.link-title",
                "result_title": "h2.body-2",

                "details_title": "h1",
                "last_update": "span.date-news",
                "content": "div.body-2.blockreadmore.body-content.readmore-section.readmore-collapsed",
                "pkg_anchor": "a.body-2.text-truncate",
                "pkg_id": "a.body-2.text-truncate",
                "publisher": "span.body-2 a[rel='tag']",
                "size": "div.info-block.scora:has(span.gray:has-text('Size')) >> span.body-2:not(.gray)",
                "version": "div.info-block.scora:has(span.gray:has-text('Version')) >> span.body-2:not(.gray)",
                "mod": "span.body-2 p",
                "download": "a.download-button"
            }
        },

        {
            "name": "getmodsapk",
            "base_url": "https://getmodsapk.com",
            "search": "https://getmodsapk.com/search?query={apk_name}",
            "selectors": {
                "results": "a.bg-white",
                "result_title": "h3.font-semibold",

                "details_title": "h1.text-2xl",
                "version": "div.info-grid-card-custom:nth-of-type(2) p.text-sm.md\\:text-xl.font-bold",
                "last_update": "div.flex.items-center.dark\\:text-gray-300",
                "publisher": "div.info-grid-card-custom:nth-of-type(4) p.text-sm.md\\:text-xl.font-bold",
                "size": "div.info-grid-card-custom:nth-of-type(7) p.text-sm.md\\:text-xl.font-bold",
                "pkg_anchor": "div.info-grid-card-custom:nth-of-type(8) a",
                "mod": "div.pl-8.pb-3.prose ul",
                "content": "div.post-content.text-gray-900",
                "download": "a[href*='/download']"
            }
        },
        {
            "name": "apkpure",
            "base_url": "https://apkpure.com",
            "search": "https://apkpure.com/search?q={apk_name}",
            "selectors": {
                "results": "a[data-dt-recid]",
                "result_title": "p.p1",

                "details_title": "h1",
                "version": "span.version.one-line",
                "last_update": "li:has-text('Update date') div.head",
                "pkg_anchor":"div.additional-item:has-text('Available on') a.value.ga",
                "publisher": "a.developer.one-line",
                "download": "a.btn.normal-download-btn.da.dt-main-download-btn",
                "size": "a.btn.normal-download-btn.da.dt-main-download-btn",
                "content": "div.show-more",
            }
        },
        {
            "name": "filecr",
            "base_url": "https://filecr.com",
            "search": "https://filecr.com/search/?q={apk_name}",
            "selectors": {
                "results": "a.card_title__az7G7",
                "result_title": "a.card_title__az7G7",

                "details_title": 'div.info_item__0IxQW:has-text("File name") span.info_data__N609l',
                "publisher": 'div.info_item__0IxQW:has-text("Created by") span.info_data__N609l a',
                "pkg_anchor": 'div.info_item__0IxQW:has-text("Google Play") span.info_data__N609l a',
                "version": 'div.info_item__0IxQW:has-text("Version") span.info_data__N609l',
                "last_update": 'div.info_item__0IxQW:has-text("Release Date") span.info_data__N609l',
                "mod": "span.info_data__N609l.info_green__1WTdc",
                "size": "div.download-size",
                "content": "article.article",
            }
        },
        {
            "name": "apkcombo",
            "base_url": "https://apkcombo.com",
            "search": "https://apkcombo.com/search/{apk_name}/",
            "selectors": {
                "results": "a.l_item",
                "result_title": "span.name",

                "details_title": "h1 a[title]",
                "publisher": "//div[@class='information-table']//div[@class='item'][.//div[@class='name' and contains(text(),'Developer')]]//div[@class='value']",
                "version": "//div[@class='information-table']//div[@class='item'][.//div[@class='name' and contains(text(),'Version')]]//div[@class='value']",
                "last_update": "//div[@class='information-table']//div[@class='item'][.//div[@class='name' and contains(text(),'Update')]]//div[@class='value']",
                "pkg_anchor": "div.item:has-text('Google Play ID') div.value a.is-link",
                "pkg_id":"div.item:has-text('Google Play ID') div.value a.is-link",
                "download": "a.button.is-success.is-fullwidth",
                "size": "span.fsize span",
                "content": "div.text-description.ton",
            }
        },
    ]

    @staticmethod
    def similarity(a: str, b: str) -> float:

        def clean(text: str) -> str:
            text = text.lower()
            text = re.sub(r"\bv?\d+(\.\d+)*\b", "", text)
            text = re.sub(r"\bmod( apk)?\b", "", text)
            text = re.sub(r"[^a-z0-9\s]", "", text)
            return text.strip()

        a_clean = clean(a)
        b_clean = clean(b)

        if a_clean == b_clean:
            return 1.0
        if a_clean in b_clean:
            return 0.95

        return SequenceMatcher(None, a_clean, b_clean).ratio()

    @staticmethod
    async def search_site(page, site, app_name):
        search_url = site["search"].format(apk_name=app_name.replace(" ", "+").lower())
        await page.goto(search_url, timeout=30000)

        results = await page.query_selector_all(site["selectors"]["results"])
        collected = []

        for r in results[:5]:
            if site["selectors"]["result_title"]:
                title_el = await r.query_selector(site["selectors"]["result_title"])
                title = await title_el.inner_text() if title_el else await r.inner_text()
            else:
                title = await r.inner_text()
            href = await r.get_attribute("href")
            collected.append((title.strip(), href))

        return collected

    @staticmethod
    def parse_date(date_str: str) -> str | None:
        if not date_str:
            return None
        match = re.search(r"([A-Za-z]{3,9} \d{1,2}, \d{4})", date_str)
        if not match:
            return None

        date_str = match.group(1)
        formats = [
            "%B %d, %Y",
            "%d %B %Y",
            "%b %d, %Y",
            "%Y-%m-%d",
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None


    async def extract_metadata(self,page, site, href):
        full_url = urljoin(site["base_url"], href)
        await page.goto(full_url, timeout=30000)
        meta = {}

        for key, selector in site["selectors"].items():
            if key in ["results", "result_title"]:
                continue
            try:
                el = await page.query_selector(selector)
                if el:
                    if key in ["pkg_anchor", "download"]:
                        dwnld_href = await el.get_attribute("href")
                        meta[key]=urljoin(site["base_url"], dwnld_href)
                    elif key == "last_update":
                        raw_date = await el.inner_text()
                        meta[key] = self.parse_date(raw_date)
                    else:
                        meta[key] = (await el.inner_text()).strip()
            except Exception as e:
                print(f"⚠️ Skipped {key} for {site['name']}: {e}")

        meta["url"] = full_url

        m_pkg_id = meta.get("pkg_id")
        if not m_pkg_id or not m_pkg_id.strip():
            url = meta.get("pkg_anchor", "")
            match = re.search(r"[?&]id=([^&]+)", url)
            m_pkg_id = match.group(1).strip() if match and match.group(1) else None
        meta["pkg_id"] = m_pkg_id

        return meta

    async def parse_leak_data(self, query: Dict, context: BrowserContext):
        await context.route("**/*", lambda route: route.abort() if route.request.resource_type in {"image", "media", "font", "stylesheet", "texttrack", "video", "audio"} else route.continue_())

        page = await context.new_page()
        import re
        if "playstore" in query and query["playstore"]:
            v = str(query["playstore"]).strip()
            if v.startswith("http://") or v.startswith("https://") or "play.google.com" in v:
                url = v
                m = re.search(r"id=([a-zA-Z0-9._-]+)", v)
                pkg_name = m.group(1) if m else ""
            elif re.match(r"^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+$", v):
                pkg_name = v
                url = f"https://play.google.com/store/apps/details?id={v}"
            else:
                return
        else:
            return

        await page.goto(url, timeout=60000)
        app_name = await page.inner_text("h1 span[itemprop='name']", timeout=30000)

        all_best_results = []

        for site in self.APK_SITES:
            try:
                collected = await self.search_site(page, site, app_name)

                best_site_result = None
                best_site_score = 0

                for title, href in collected:
                    score = self.similarity(app_name, title)
                    if score > best_site_score:
                        best_site_score = score
                        best_site_result = (site, title, href, score)

                if best_site_result:
                    all_best_results.append(best_site_result)

            except Exception as e:
                print(f"❌ Error searching {site['name']}: {e}")

        found_cards: List[apk_model] = []
        found_entities: List[apk_model] = []
        for site, title, href, score in all_best_results:
            try:
                meta = await self.extract_metadata(page, site, href)
            except Exception as _:
                continue

            card_data = apk_model(
                m_app_name=meta.get("details_title", title),
                m_app_url=meta.get("url") or "",
                m_package_id=meta.get("pkg_id") or pkg_name,
                m_mod_features=meta.get("mod") or "",
                m_network="clearnet",
                m_version=meta.get("version") or "",
                m_download_link=[meta.get("download")] if meta.get("download") else [],
                m_content_type=["apk"],
                m_latest_date=str(meta.get("last_update"))
            )

            found_cards.append(card_data)
            self.append_apk_data(card_data)

        self._card_data.extend(found_cards)
        self._entity_data.extend(found_entities)

        model = apk_data_model(base_url=self.base_url, content_type=["cracked"])
        model.cards_data = self.card_data
        return model
