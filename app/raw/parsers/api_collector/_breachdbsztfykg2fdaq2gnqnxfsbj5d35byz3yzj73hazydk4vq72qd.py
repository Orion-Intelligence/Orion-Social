import re
from abc import ABC
from typing import Dict, List

from crawler.crawler_instance.local_interface_model.api.api_collector_interface import api_collector_interface
from crawler.crawler_instance.local_interface_model.api.api_data_model import api_data_model
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.leak_model import leak_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType
from crawler.crawler_services.shared.helper_method import helper_method
from playwright.async_api import BrowserContext


class _breachdbsztfykg2fdaq2gnqnxfsbj5d35byz3yzj73hazydk4vq72qd(api_collector_interface, ABC):
    _instance = None

    def __init__(self):
        self._initialized = None
        self._card_data = []
        self._entity_data = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_breachdbsztfykg2fdaq2gnqnxfsbj5d35byz3yzj73hazydk4vq72qd, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @property
    def developer_signature(self) -> str:
        return "Muhammad Hassan Arshad: owEBeAKH/ZANAwAKAbKjqaChU0IoAcsxYgBoei5jVmVyaWZpZWQgZGV2ZWxvcGVyOiBNdWhhbW1hZCBIYXNzYW4gQXJzaGFkCokCMwQAAQoAHRYhBD5p3c9aqX5fJ9SIZbKjqaChU0IoBQJoei5jAAoJELKjqaChU0Io2i8QAKRGGxAbMJGV97ym5wcir4mn2es2/npd+MFDa/LZFnkcoPOP9/fKtg9pZ1a2PVa0h9s5ewU6wGJ4HIvjP/2gxd1maDIjv6IM+5mtlpJvQJhzoqHdAg//IRwJU5QO2krqxBQrtcvNwfkW1IoNSEaJCr0EmXht3rkGhkJ3J3XqEvrBeH0DtaZLnCLOJ3eTIRleqbBOUdq2Uf9hDZZY9rdqynjjsADo1lhchdyPjwBz1g8M/q1Ud3sTUA+/8gas5l15jR9SGQZxbgnzZRjG19oq5GAhLwUYgKuoH+zANQEB7leF9jBudzYz2Ey/4BglnVE6kszUo7RxPoqtNOFvq6WzCcRKPLO323sLfFYtwXDwvJ0iviVTOwrbXlA80GFANcAbSR76nN0XrsaLM2L/KT6oe0wTVq35j1QZnt4Jq5PWALA8hQNr7w1KtuwnpN5PmE741h+9OfZP2ogd9ERbmGb10DROsd9t4RL4hpxpsCoekHRbLI3XmHFZqFAB/GgF194Tmh3LcoIAcwOYty/PVDuPYMGMmm5Nttg2vvVrMg82P0LeOrIN2Mq03HCiZm/HaOvePniPg+EeaWPMiVmGWvCJUOMI/TJRz4jVLR4BUlvoiUSNBWrJhxMRQZpViam2rVUaojPaZhzoIF4sqS6hYqzZbbXHwtYjJfNOHh00gucABJHw=gmDH"

    @property
    def base_url(self) -> str:
        return "http://breachdbsztfykg2fdaq2gnqnxfsbj5d35byz3yzj73hazydk4vq72qd.onion"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(m_fetch_proxy=FetchProxy.TOR, m_fetch_config=FetchConfig.PLAYRIGHT, m_threat_type=ThreatType.API)

    @property
    def card_data(self) -> List[leak_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def append_leak_data(self, leak: leak_model, entity: entity_model):
        self._card_data.append(leak)
        self._entity_data.append(entity)

    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    async def parse_leak_data(self, query: Dict[str, str], context: BrowserContext):
        print(":::::::::::::::::::::::::::::::::::::: x0-1 ", flush=True)
        p_data_url = self.base_url
        email = query.get("email", "")
        username = query.get("username", "")
        print(":::::::::::::::::::::::::::::::::::::: x0-2 ", flush=True)

        collector_model = api_data_model(base_url=p_data_url, content_type=["email", "username"])
        print(":::::::::::::::::::::::::::::::::::::: x0-3 ", flush=True)
        combined_records = set()
        print(":::::::::::::::::::::::::::::::::::::: x0-4 ", flush=True)
        email_list = set()
        print(":::::::::::::::::::::::::::::::::::::: x0-5 ", flush=True)
        username_list = set()
        print(":::::::::::::::::::::::::::::::::::::: x0-6 ", flush=True)

        page = await context.new_page()
        print(":::::::::::::::::::::::::::::::::::::: x0-7 ", flush=True)
        await page.goto(p_data_url)
        print(":::::::::::::::::::::::::::::::::::::: x1 ", flush=True)

        print(":::::::::::::::::::::::::::::::::::::: x3 ", flush=True)
        await page.locator("#SearchType").wait_for(timeout=120000)

        print(":::::::::::::::::::::::::::::::::::::: x4 ", flush=True)
        for search_type, query_value in [("Username", username), ("Email", email)]:
            if not query_value:
                print(":::::::::::::::::::::::::::::::::::::: x5 ", flush=True)
                continue

            try:
                await page.locator("#SearchType").select_option(value=search_type)
                search_box = page.locator("#TxtSearch")
                await search_box.fill(query_value)
                search_button = page.locator("#BtnSearch")
                await search_button.click()

                print(":::::::::::::::::::::::::::::::::::::: x6 ", flush=True)
                result_panel_locator = page.locator(".ResultPanel")
                warning_locator = page.locator("div.WarningPanel", has_text="Nothing found")
                if await warning_locator.is_visible():
                    print(":::::::::::::::::::::::::::::::::::::: x7", flush=True)
                    return []
                try:
                    await result_panel_locator.wait_for(timeout=5000)
                except:
                    pass

                print(":::::::::::::::::::::::::::::::::::::: x8 ", flush=True)
                spans = await result_panel_locator.locator("span").all()
                public_records = [
                    (await span.text_content()).split("-->", 1)[0].strip()
                    for span in spans if "-->" in (await span.text_content())
                ]
                combined_records.update(public_records)

                if search_type == "Email":
                    email_list.add(query_value)
                else:
                    username_list.add(query_value)
            except Exception as _:
                print(":::::::::::::::::::::::::::::::::::::: x9 ", flush=True)
                continue

        print(":::::::::::::::::::::::::::::::::::::: x10 ", flush=True)
        if combined_records:
            card_data = leak_model(
                m_title=f"Records for provided queries",
                m_important_content=f"Records were found in a data breach.",
                m_weblink=[],
                m_screenshot="",
                m_content="",
                m_base_url=self.base_url,
                m_network=helper_method.get_network_type(self.base_url),
                m_url=p_data_url,
                m_content_type=["stolen"],
                m_dumplink=list(combined_records),
            )

            entity_data = entity_model(
                m_scrap_file=self.__class__.__name__,
                m_email=list(email_list),
                m_name=", ".join(username_list)
            )
            self.append_leak_data(card_data, entity_data)
            collector_model.cards_data = self.card_data
            return collector_model
