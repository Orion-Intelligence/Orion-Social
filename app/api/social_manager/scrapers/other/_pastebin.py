import re
import random
from datetime import datetime
from abc import ABC
from typing import List
from collections import OrderedDict
from playwright.sync_api import Page

from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method


class _pastebin(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self.m_seed_url = "https://pastebin.com/u/lemueltra"
        self._initialized = None
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._title_seen = OrderedDict()

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
        return "Muhammad Huzaifa:mQINBGmuceABEADJSBBZ0rvBo7x2RlxNhGTFshceCzBgTxvJ3Qu72UxdCIwDXRIH9Zmi+XJCYIPvuQjZWM8cYyJ48JIS4ewzQOwFjpwnPRmVnSn0bkvzv+KoannM1bIH+67aZfEkc4WB+TwFTVozypypw8oNPR9GXZHWoynwGMZVUyjam2Btzz/HOZmmuQov8YfgbdRN0gW+uJpEHYi9q3eFhDriPENr8Woy/1z/f0SL66EVUT9n0xROFizeaZh6jdL8D2PTAngYm5kZ12n7fIHquZ//WFypTi+iJHO/rl6I9K20N3SQN8gW3SG1QeEJST8yscgYSxIgtUo14qQNxUFCEeNv7J7MxBfAjiqBkRBAnCffhXZO4LqiVlYUM7UENnbTM+NFvX+D7SeST18jIstlvnWwN3QeTIn79sahv1Kzj45ATi3nY3wcq5I7IIgm0W5AItvZyzzQAHgdmiXWaa5HV7vvMW9gIkwD9X3/oReEdjK4xrId2CCiuAmd0BYTalTvs5UFDrXcweFC7d8cm7MpmjJHujP7DpsyYhxD11uCDQWS8CV2GsIKuL1qT7bzUcpu0IVOaBy4tlprxsq3uL9hv/WGBTkFcWuhmY1mawcRcGrjDNxelbt32Q8ZqAwdoEDbFcH/z+FmAZHjl/JD1K+LOX8aVw+U6qSG0A6hut/vaxEAsCDjQ7/S3QARAQABtCtNdWhhbW1hZCBIdXphaWZhIDxtaHV6YWlmYTE4MDMwNUBnbWFpbC5jb20+iQJRBBMBCgA7FiEEUuyWkNNHiBlQjp+vMbq7PAvKlBUFAmmuceACGwMFCwkIBwICIgIGFQoJCAsCBBYCAwECHgcCF4AACgkQMbq7PAvKlBWKHQ//bcdHfuqsainBoOZ6ZdYogAp5VnDfix4V45OBfDxyTGek/E5BFXZErVUDgTTvXl2GhLFSKm7NMsqnXtYtHdKuKTsxZSqzqRPbZZs0kJ0GCO4NdyYULGWZP06dG3R9ed2tzsnaVafCndcSqoyafWsZyeweoHGbxi4VeWmrz675HjHqo1Oclg7itTDUn8R63Tw1hnbvzLEkKZoC+WxuCx3ScGZzmnInHwZpyl0hiSkqxpHjS6NDUhhKsYGD2rJkxPXNjkkixt2NSoSQ4ul/w649qi1BfVIWKvSz403Q2Adw5yJiLIlwHE2zPvmpLg/8RHTgq/LN+s5scAlaMO/NHvaIFlaMawxOjl/U5AHnFUBJWYjPipsNgbb2X/X/drAUo8Dy4MON8oZpPZIFW0jO8t6bM97KzCaGpELHJnNR8y/Ls5Lzxm3Nctf0V7P946WqhQWQ3OAFZ634lIR4dNmoSFeFDOEpUf1rZzlCPtj+8GpEcx9sVDmpvsi+F8U4A+yBfQzcH3AnHoJgdj2kd7SfLklojEmRDuHMOcaTMiqA/iSR0ScRm/uxnl1c/BLPOgiX5Zbg7OcoWYGtC9/ou4O25WiSgnX0YIu0a1GL0weGPIWsfNr4N3Y4eY2hLsyjomN8IFILU99D3MeyQGQPKBOVhuAKW3hx5SptlPtm5BMKApV6blq5Ag0Eaa5x4AEQAOTl5oZxyCcH9D4wkzP7VyuER27rVqqhdu4yDerEa0kzMz+0mxlVakryIp3k9w5mMNOk32rNk3fZcg9sW/f80l73TkET2bfkbeyf0us1mw1srk5x5rjpi1jiwrryb115ub+EtGN6plr5pZVUwwbeEVkn0llesvQ5CmPYCk7N0NwBN/Kt93yNk5taEZUf7h7zqSRIfIcytFA1camMvu7SpA8jX/v5xT4XDeDn2632REVgEKyWbhAZp9RlsUVTaBdZ0NhAh+AlRu71EjGMwswGxDjssGTerDcuzbqp3hh1vcOrsk9WNgS8ZOpyK8KPn1aSFmdo+gHxkF+eMF8DTdE6Gdnv38fdqxaEC9e4rxUgc/YQc88jgSrFXQsj2h1MkYIr6jHRszpcieVBjrx4qC83YiDW3AYqcQDPk/MkxaUWKSYGCAf3rj1onNRdeFdyovc3ZQDeFz9rtORS+e5TuykFApwkiFGnpiaIpvXPRA5N1TNbrNpu2CwC1eS9xPT7U6RCgSLWJ5ivCf0flDLNMYOk/uocJELamPTqMotQOmJoFJ4i9PX2OwvVop/Hg5soGntJA4/VhtmXQmz+uMtMb8xreFN/h5c/3W1b38oUk06hB1c+DrqS2DvoT1gPRRFIAjK1VsWLqAIw1//W/kw9uZpgjpO5BHLL18UCAH4K7fihS0bzABEBAAGJAjYEGAEKACAWIQRS7JaQ00eIGVCOn68xurs8C8qUFQUCaa5x4AIbDAAKCRAxurs8C8qUFRTjEACGa/Zn82FUpPBkjN1i19GFDEIkqZIIOJCWcwaR8MASdjdtN/WQlBNlC8cT/79BGoKILjodiu+DYTteshNZPJH0wNM6BvvlCTNeA8VoNOgBUDDq16FBRxe/vfsrERRsAbtpQqGVACmpKJRgDQwz2MfUHjM2pnioqyytsQo08zMPuVjVA/daBhDaNqmC0laTlhB7MkD+0nIpP8JHFkVcUNgRnhjy058/ap7wQmsJ/4Y0TWtG0rQETtzD+0MueWDM6FJaXf+jqbJM10gz3MT8CCU10zNnGqKmXW9EABFBO7PL/1GZ3GOWWFj1NrZJef7NS2ngyoTFf2q9/CJtgA7R+QgenRMiDGTaBHBj531CPiscieb5iyb8/7fD7vrsNMpQ1z+9ZtIej/Ltw5C2eX7Exw39XCpx5ljzlJYiHMErOipXEcnjeXH94YJlfr4YEbOMqYdGAPr/fnSqO5XFHW7jxI8JLrgl+YuqTIy0yZO2CQqXGgNan3NVIIDOH1fL0tnsnZUwUHqYReQki5qyH1389KR4y+4Nfv3q/GywGlIT1AR7PaSX0rnU4rfWPzBhcucMq+uqD1M1Q7ShjWNrwRVpoGcFpYtQYcdKol36LzA3VqYTiGHKJp2JOI83b83B4Efh9lDPL0nYKoyfTsEaKmfy737NKGvrQyXcVtAycLqtV/n3Eg===OU1e"
    @property
    def base_url(self) -> str:
        return "https://pastebin.com"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.NONE,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_resoource_block=False,
            m_threat_type=ThreatType.PASTEBIN,
            m_rule_type=RuleType.PASTEBIN,
            m_social_data_type=getattr(self, "m_social_data_type", SocialDataType.DEFAULT),
        )

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def invoke_db(self, command: int, key: str, default_value, expiry: int | None = None):
        return self._redis_instance.invoke_trigger(command, [key + self.__class__.__name__, default_value, expiry])

    def contact_page(self) -> str:
        return "https://pastebin.com/contact"

    @staticmethod
    def _safe_text(locator, default: str = "") -> str:
        try:
            return (locator.inner_text() or "").strip()
        except Exception:
            return default

    @staticmethod
    def _parse_paste_date(raw_date: str):
        try:
            clean_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', raw_date or "", flags=re.IGNORECASE)
            clean_date = re.sub(r'\(.*?\)', '', clean_date).strip().title()
            month = clean_date.split()[0]
            fmt = "%b %d, %Y" if len(month) <= 3 else "%B %d, %Y"
            return datetime.strptime(clean_date, fmt).date()
        except Exception:
            return datetime.now().date()

    @staticmethod
    def _extract_profile_assets(page: Page) -> dict:
        try:
            return page.evaluate("""() => {
                const cleanUrl = value => {
                    if (!value) return '';
                    const match = String(value).match(/url\\(["']?([^"')]+)["']?\\)/);
                    const raw = match ? match[1] : String(value);
                    if (!raw || raw.startsWith('data:') || /^(none|initial|inherit|unset)$/i.test(raw.trim())) return '';
                    try { return new URL(raw, location.href).href; } catch (_) { return raw; }
                };
                const isGeneric = value => /favicon|logo|pastebin\\.com\\/(i|themes)\\//i.test(value || '');
                const firstAttr = (selectors, attr) => {
                    for (const selector of selectors) {
                        const node = document.querySelector(selector);
                        const value = node?.getAttribute(attr) || node?.[attr] || '';
                        const url = cleanUrl(value);
                        if (url && !isGeneric(url)) return url;
                    }
                    return '';
                };
                const bgUrl = selectors => {
                    for (const selector of selectors) {
                        const node = document.querySelector(selector);
                        if (!node) continue;
                        const url = cleanUrl(getComputedStyle(node).backgroundImage);
                        if (url && !isGeneric(url)) return url;
                    }
                    return '';
                };
                const profileIcon = firstAttr([
                    '.user-icon img',
                    '.user-avatar img',
                    '.avatar img',
                    'img.avatar',
                    'img[alt*="avatar" i]',
                    'img[alt*="profile" i]'
                ], 'src');
                const coverpage = firstAttr([
                    '.profile-cover img',
                    '.user-cover img',
                    '.cover img',
                    'img[alt*="cover" i]'
                ], 'src') || bgUrl(['.profile-cover', '.user-cover', '.cover']);
                return {profileIcon, coverpage};
            }""") or {}
        except Exception:
            return {}

    def _append_profile_info(self, page: Page | None = None):
        username = self.seed_url.rstrip("/").split("/")[-1]
        profile_assets = {}
        if page is not None:
            try:
                if page.url.rstrip("/") != self.seed_url.rstrip("/"):
                    page.goto(self.seed_url, wait_until="domcontentloaded", timeout=25000)
                profile_assets = self._extract_profile_assets(page)
            except Exception:
                profile_assets = {}
        content_type = "profile_info"
        card_data = social_model(
            m_title=username,
            m_channel_url=self.seed_url,
            m_sender_name=username,
            m_url=self.seed_url,
            m_weblink=[self.seed_url],
            m_content=username,
            m_content_type=["social_collector", "pastebin_profile", content_type],
            m_network="clearnet",
            m_date=datetime.now().date(),
            m_message_id=username,
            m_platform="pastebin",
            m_group_name=username,
            m_img_src=profile_assets.get("profileIcon") or None,
            m_coverpage=profile_assets.get("coverpage") or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))

    def _is_target_hash_request(self, data_type: SocialDataType) -> bool:
        return data_type == SocialDataType.COMMENTS and bool(str(getattr(self, "m_hash_id", "") or "").strip())

    def parse_leak_data(self, page: Page):
            self._card_data = []
            self._entity_data = []
            try:
                data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
                if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL, SocialDataType.FOLLOWERS, SocialDataType.FOLLOWING):
                    self._append_profile_info(page)
                    return
                if data_type in (SocialDataType.VIDEOS, SocialDataType.SHORTS):
                    return
                target_hash = self._is_target_hash_request(data_type)

                url_lists = []

                if "/u/" not in self.seed_url:
                    url_lists.append(self.seed_url)
                else:
                    links = page.locator("td:has(span) a")

                    for i in range(links.count()):
                        href = links.nth(i).get_attribute("href")
                        if href:
                            full_url = href if href.startswith("http") else self.base_url + href
                            url_lists.append(full_url)

                limit = max(1, min(int(getattr(self, "m_item_limit", 10) or 10), 100))
                if not target_hash:
                    url_lists = url_lists[:limit]

                for url in url_lists:
                        try:
                            page.goto(url, wait_until="load", timeout=25000)
                            page.wait_for_timeout(750)
                        except:
                            pass

                        title = self._safe_text(page.locator("div.info-top")) or "Pastebin post"

                        username = self._safe_text(page.locator("div.info-bar div.info-bottom div.username a").first)

                        raw_date = self._safe_text(page.locator("div.info-bar div.info-bottom div.date").first)
                        date = self._parse_paste_date(raw_date)

                        tags_locator = page.locator("div.tags a")
                        if tags_locator.count():
                            tags = tags_locator.all_inner_texts()
                        else:
                            tags = []

                        visits_locator = page.locator("div.visits")
                        raw_visits = self._safe_text(visits_locator)
                        visits = raw_visits.strip() if raw_visits else ""

                        expire_locator = page.locator("div.expire")
                        raw_expire = self._safe_text(expire_locator)
                        expire = raw_expire.strip() if raw_expire else ""

                        try:
                            source = page.locator("ol.diff , .post-view ol").first.inner_text(timeout=5000) or ""
                        except:
                            source = ""

                        m_content = source.replace("\xa0", " ").strip()

                        cleaned = source.replace("\xa0", " ")
                        cleaned = re.sub(r'[ \t]+', ' ', cleaned)

                        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                        ip_pattern = r'\b\d{1,3}(?:\.\d{1,3}){3}\b'
                        domain_pattern = r'\b(?:https?://[^\s@]+|www\.[^\s@]+)'

                        emails = list(set(re.findall(email_pattern, cleaned)))
                        ips = list(set(re.findall(ip_pattern, cleaned)))
                        domains = list(set(re.findall(domain_pattern, cleaned)))

                        content_type = ["social_collector", "pastebin_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"]
                        if helper_method.is_code(m_content):
                            content_type.append("code")

                        card_data = social_model(
                            m_title=title,
                            m_channel_url=self.seed_url,
                            m_sender_name=username,
                            m_url=page.url,
                            m_message_sharable_link=page.url,
                            m_message_id=page.url.rstrip("/").split("/")[-1],
                            m_content=m_content,
                            m_network="clearnet",
                            m_content_type=content_type,
                            m_platform="pastebin",
                            m_date=date,
                            m_post_tags=tags,
                            m_post_views=visits,
                            m_views=visits,
                            m_post_expiry=expire,
                            m_group_name=username,
                            m_code_snippet=[m_content] if "code" in content_type and m_content else [],
                            m_scrap_file=self.__class__.__name__,
                            m_weblink=domains or [page.url],
                        )
                        if target_hash:
                            if self._is_requested_hash_id(card_data):
                                self.append_leak_data(card_data, entity_model(m_username=[username], m_ip=ips, m_email=emails))
                                return
                            continue
                        if self._is_requested_hash_id(card_data):
                            break

                        entity_data = entity_model(
                            m_username=[username],
                            m_ip=ips,
                            m_email=emails,
                        )

                        self.append_leak_data(card_data, entity_data)

            except Exception as ex:
                log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
