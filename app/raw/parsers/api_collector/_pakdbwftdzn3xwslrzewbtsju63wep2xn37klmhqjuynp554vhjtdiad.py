import re
from abc import ABC
from typing import Any, Dict, List, Tuple

from playwright.async_api import BrowserContext
from crawler.crawler_instance.local_interface_model.api.api_collector_interface import api_collector_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType


class _pakdbwftdzn3xwslrzewbtsju63wep2xn37klmhqjuynp554vhjtdiad(api_collector_interface, ABC):
    _instance = None

    def __init__(self):

        self._card_data = []
        self._entity_data = []

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super(_pakdbwftdzn3xwslrzewbtsju63wep2xn37klmhqjuynp554vhjtdiad, cls).__new__(cls)
        return cls._instance

    def _prune_empty(self, data: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = {}
        for k, v in data.items():
            if v is None:
                continue
            if v == "":
                continue
            if v == []:
                continue
            if v == {}:
                continue
            cleaned[k] = v
        return cleaned

    @property
    def developer_signature(self) -> str:

        return "Syed Ibrahim : owEBbgKR/ZANAwAKAZ6k986TaqHrAcsnYgBogoHBVmVyaWZpZWQgZGV2ZWxvcGVyOiBTeWVkIElicmFoaW0KiQIzBAABCgAdFiEE0cDJTTL9lGNCNy3mnqT3zpNqoesFAmiCgcEACgkQnqT3zpNqoeu+UxAAvORjme5u4ZXhva6MkNXPwRHrKLbhZrBBYHgkDra+reoSSRQnMQTlEGWEhRiBi3wGo4MyC2xwhCjRW1raFddBnv03LA59ro978LafPwpEO6cQYxnpqI8nDh6TIEbcJi2GLPIOc4xZm79GvxVZ6b9t5zoaNdSUPv/AwidjXGU4ACIkDo9LQW0RLiVUq8wvhPJRcvvwpmKGwLc9XRWSG95Vv172cv6KCh14EAW90sXSaDc4nIP9sr13j3YN1XGmQwTtmQo8ynmZpZ3JydmUud79ZnB+CfXZXKRehDlSfnTQH5TezsZCpshv5KbtuYwVsqgp/zDSMSZwGtgeaeD3M/yYgRdxbu0yt9RQ74yiwiqzBWa6yEkkECAkAb9QwRXGIqX3oWLFMadiBkCFMaILl+NH4phAVB4lual3H7bZEBgNasOjNm+SYqf/8FJrhBCSjVkLpkpQ71oEBUX06vX+tj2hXW42ZjWm4Lx9qHPh5JYyp9Th5DhnYONVvK96DQHxjYIpqbDTigVCS/rN6PFHolJHOFFivnzYqGeWZEzoI9U+2JhmuDwStKBMNWE+NWJHyyNsOFqEZ1Murl5sBpJEMeC4J4Vn//lPvQAo24hAULJAmOT9CjT00DdnXRdyl602fv0HfwzPf78NQ3LUuabyTLMQUgDKm8Gg8LlenlraOovjXgw==s7Wx"

    @property
    def base_url(self) -> str:

        return "http://pakdbwftdzn3xwslrzewbtsju63wep2xn37klmhqjuynp554vhjtdiad.onion"

    @property
    def rule_config(self) -> RuleModel:

        return RuleModel(m_fetch_proxy=FetchProxy.TOR, m_fetch_config=FetchConfig.PLAYRIGHT, m_threat_type=ThreatType.API)

    @property
    def card_data(self) -> List[dict]:

        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:

        return self._entity_data

    def append_entity_data(self, entity: entity_model):
        self._card_data.append(self._prune_empty(entity.model_dump(exclude_none=True)))
        self._entity_data.append(entity)

    @property
    def cards_data(self) -> List[dict]:
        return self._card_data

    def model_dump(self) -> Dict[str, List[dict]]:
        return {"cards_data": self._card_data}

    import re
    from typing import Dict, Tuple

    async def parse_leak_data(self, query: Dict[str, str], context: "BrowserContext"):
        p_data_url = self.base_url
        raw_value = (query.get("pak_query") or "").strip()

        police_url = (
            "http://pakdbwftdzn3xwslrzewbtsju63wep2xn37klmhqjuynp554vhjtdiad.onion"
            "/databases/police.php"
        )
        familytree_url = (
            "http://pakdbwftdzn3xwslrzewbtsju63wep2xn37klmhqjuynp554vhjtdiad.onion"
            "/databases/familytree.php"
        )
        landline_url = (
            "http://pakdbwftdzn3xwslrzewbtsju63wep2xn37klmhqjuynp554vhjtdiad.onion"
            "/databases/landline.php"
        )

        self._card_data = []
        self._entity_data = []

        def normalize_cnic(s: str) -> str:
            return re.sub(r"[\s\-]+", "", s).strip()

        def digits_only(s: str) -> str:
            return re.sub(r"\D+", "", s)

        def normalize_mobile(s: str) -> str:
            d = digits_only(s)
            if d.startswith("92"):
                d = d[2:]
            if len(d) == 10 and d.startswith("3"):
                d = "0" + d
            return d

        def classify(s: str) -> Tuple[str, str]:
            c = normalize_cnic(s)
            if re.fullmatch(r"\d{13}", c):
                return "cnic", c
            d = digits_only(s)
            if not d:
                return "unknown", s
            d_no92 = d[2:] if d.startswith("92") else d
            if (len(d_no92) == 11 and d_no92.startswith("03")) or (len(d_no92) == 10 and d_no92.startswith("3")):
                return "mobile", normalize_mobile(s)
            if len(d) >= 7:
                return "landline", d
            return "unknown", s

        async def fetch_rows(page: "Page", url: str, form_action: str, table_selector: str, value: str) -> list[
            list[str]]:
            try:
                await page.goto(url, wait_until="domcontentloaded")
                form = f'form[action="{form_action}"][method="post"]'
                inp = f'{form} input[name="search_query"]'
                await page.wait_for_selector(inp, timeout=15_000)
                await page.click(inp, click_count=3)
                await page.keyboard.press("Backspace")
                await page.type(inp, value, delay=15)
                await page.press(inp, "Enter")
                await page.wait_for_selector(table_selector, timeout=20_000)
                await page.wait_for_selector(f"{table_selector} tbody", timeout=3_000)
                trs = await page.query_selector_all(f"{table_selector} tbody tr")
                rows: list[list[str]] = []
                for tr in trs:
                    tds = await tr.query_selector_all("td")
                    if not tds:
                        continue
                    cells = [((await td.inner_text()) or "").strip() for td in tds]
                    if any(cells):
                        rows.append(cells)
                return rows
            except Exception:
                return []

        def append_basic(rows: list[list[str]]):
            phones: list[str] = []
            names: list[str] = []
            cnics: list[str] = []
            locations: list[str] = []
            for r in rows:
                if len(r) < 4:
                    continue
                if r[0]:
                    phones.append(r[0])
                if r[1]:
                    names.append(r[1])
                if r[2]:
                    cnics.append(normalize_cnic(r[2]))
                if r[3]:
                    locations.append(r[3])
            if phones or names or cnics or locations:
                self.append_entity_data(
                    entity_model(
                        m_phone_numbers=phones,
                        m_name=names[0] if names else "",
                        m_id_card_number=cnics,
                        m_location=locations,
                    )
                )

        kind, value = classify(raw_value)
        page = await context.new_page()

        if kind == "landline":
            rows = await fetch_rows(page, landline_url, "/databases/landline.php", "table.api-response", value)
            append_basic(rows)
            return self

        main_rows = await fetch_rows(page, p_data_url, "/index.php", "table.api-response",
                                     value if kind in ("mobile", "cnic") else raw_value)
        append_basic(main_rows)

        if kind == "mobile":
            police_rows = await fetch_rows(page, police_url, "/databases/police.php", "table.api-response", value)
            region: list[str] = []
            district: list[str] = []
            station: list[str] = []
            record: list[str] = []
            pname: list[str] = []
            contact: list[str] = []
            pcnic: list[str] = []
            officer: list[str] = []
            status: list[str] = []
            offense: list[str] = []
            for r in police_rows:
                if len(r) < 10:
                    continue
                region.append(r[0])
                district.append(r[1])
                station.append(r[2])
                record.append(r[3])
                pname.append(r[4])
                contact.append(r[5])
                pcnic.append(normalize_cnic(r[6]))
                officer.append(r[7])
                status.append(r[8])
                offense.append(r[9])
            if any([region, district, station, record, pname, contact, pcnic, officer, status, offense]):
                self.append_entity_data(
                    entity_model(
                        m_phone_numbers=[x for x in contact if x],
                        m_name=next((x for x in pname if x), ""),
                        m_id_card_number=[x for x in pcnic if x],
                        m_location=[" / ".join([a, b, c]) for a, b, c in zip(region, district, station) if
                                    any([a, b, c])],
                        m_region=region,
                        m_district=district,
                        m_police_station=station,
                        m_complaint_record=record,
                        m_officer_name=officer,
                        m_complaint_status=status,
                        m_offense=offense,
                    )
                )

        if kind == "cnic":
            family_rows = await fetch_rows(page, familytree_url, "/databases/familytree.php", "table", value)
            cnic_no: list[str] = []
            head: list[str] = []
            dob: list[str] = []
            fam_no: list[str] = []
            member: list[str] = []
            for r in family_rows:
                if len(r) < 5:
                    continue
                cnic_no.append(normalize_cnic(r[0]))
                head.append(r[1])
                dob.append(r[2])
                fam_no.append(r[3])
                member.append(r[4])
            if any([cnic_no, head, dob, fam_no, member]):
                self.append_entity_data(
                    entity_model(
                        m_phone_numbers=[],
                        m_name=next((x for x in member if x), "") or next((x for x in head if x), ""),
                        m_id_card_number=[x for x in cnic_no if x],
                        m_location=[],
                        m_Family_head_name=head,
                        m_dob=dob,
                        m_family_no=fam_no,
                        m_family_member_name=member,
                    )
                )

        return self
