import json
import spacy
import pycountry
import os

from spacy.language import Language
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from langdetect import detect_langs, DetectorFactory
from api.nlp_manager.pii_manager.crypto_parser import crypto_parser
from api.nlp_manager.pii_manager.pii_helper import _normalize_domain, _FILE_EXT_RE, deduplicate_key
from api.nlp_manager.pii_manager.pii_extractors import (
    extract_credentials,
    extract_hashtags_mentions,
    extract_iocs_from_text,
    extract_phone_data,
    extract_countries_from_text,
    extract_presidio_entities, extract_social_profiles, extract_currencies,
)
import time
from collections import defaultdict

os.environ["TOKENIZERS_PARALLELISM"] = "false"

SKIP_ENTITIES = {
    "AU_ABN", "UK_NINO", "AU_ACN", "US_BANK_ACCOUNT_CTX", "SG_NRIC_FIN",
    "US_SSN_STRICT", "AU_MEDICARE", "AU_TFN", "US_BANK_ROUTING_VALID"
}


class pii_controller:

    def __init__(self):
        self.analyzer = self.setup_presidio()
        self.crypto_parser = crypto_parser()
        self.nlp = spacy.load("en_core_web_trf")
        if not self.nlp.has_pipe("sentencizer"):
            self.nlp.add_pipe("sentencizer", first=True)
        self.EXCLUDED_LABELS = {"TIME", "QUANTITY", "ORDINAL", "MONEY", "DATE", "CARDINAL"}
        self.country_name_set = {country.name for country in pycountry.countries}
        with open("../../../app/raw/attacks/enterprise-attack.json", "r", encoding="utf-8") as f:
            mitre_data = json.load(f)
            self.mitre_techniques = [
                {
                    "id": ref["external_id"],
                    "name": obj.get("name", ""),
                    "type": obj.get("type", ""),
                    "keywords": f"{ref['external_id']} {obj.get('name', '').lower()}"
                }
                for obj in mitre_data.get("objects", [])
                if obj.get("type") == "attack-pattern"
                for ref in obj.get("external_references", [])
                if ref.get("source_name") == "mitre-attack"
            ]

    @staticmethod
    def setup_presidio():

        _IGNORE = {
            "PRODUCT", "LAW", "FAC", "CARDINAL",
            "QUANTITY", "DATE", "TIME", "ORDINAL", "MONEY"
        }

        @Language.component("presidio_label_filter")
        def presidio_label_filter(doc):
            doc.ents = tuple(e for e in doc.ents if e.label_ not in _IGNORE)
            return doc

        configuration = {
            "nlp_engine_name": "spacy",
            "models": [{
                "lang_code": "en",
                "model_name": "en_core_web_trf",
                "labels_to_ignore": list(_IGNORE)
            }]
        }
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()

        nlp = nlp_engine.nlp["en"]
        for pipe in list(nlp.pipe_names):
            if pipe not in ("transformer", "ner"):
                nlp.disable_pipes(pipe)

        if "presidio_label_filter" in nlp.pipe_names:
            nlp.remove_pipe("presidio_label_filter")
        nlp.add_pipe("presidio_label_filter", last=True)

        registry = RecognizerRegistry()
        registry.load_predefined_recognizers(nlp_engine=nlp_engine, languages=["en"])

        for rec in list(registry.recognizers):
            ents = set(rec.supported_entities or [])
            if ents.intersection(SKIP_ENTITIES):
                registry.remove_recognizer(rec)

        kept_entities = {
            "US_PASSPORT", "ORGANIZATION", "US_DRIVER_LICENSE", "NRP",
            "US_BANK_NUMBER", "PERSON", "MEDICAL_LICENSE", "CREDIT_CARD",
            "US_ITIN", "UK_NHS", "LOCATION", "IBAN_CODE"
        }
        for rec in list(registry.recognizers):
            ents = set(rec.supported_entities or [])
            if not ents.intersection(kept_entities):
                registry.remove_recognizer(rec)

        return AnalyzerEngine(registry=registry, nlp_engine=nlp_engine, supported_languages=["en"])

    @staticmethod
    def unify_entities(platforms_found, crypto, lang, currencies, profiles, phone_numbers, countries, iocs,
                       presidio_entities, credentials, hashtags, mentions,
                       summary=None):
        grouped = defaultdict(set)
        for ioc_type, values in iocs.items():
            grouped[ioc_type].update(values)
        grouped["PHONE_NUMBER"].update(phone_numbers)
        grouped["COUNTRY"].update(countries)
        for label, values in presidio_entities.items():
            grouped[label].update(values)
        for u, p in credentials:
            grouped["USERNAME"].add(u)
            if p:
                grouped["PASSWORD"].add(p)
        grouped["SOCIAL_MEDIA_PROFILES"] = profiles
        grouped["CRYPTO_ADDRESS"] = crypto
        grouped["LANGUAGE"] = lang
        grouped["HASHTAG"].update(hashtags)
        grouped["CURRENCIES"].update(currencies)
        grouped["MENTION"].update(mentions)
        grouped["PLATFORMS"].update(platforms_found)
        if summary:
            grouped["SUMMARY"].add(summary)

        result = {}
        for label, values in grouped.items():
            if label == "SOCIAL_MEDIA_PROFILES":
                if values:
                    existing = set(result.get("m_social_media_profiles", []))
                    existing.update(values)
                    result["m_social_media_profiles"] = sorted(existing)
                continue

            key = deduplicate_key(f"m_{label.lower().replace(' ', '_')}")
            if key in {"m_domain", "m_domains"}:
                normed_domains, file_like = set(), set()
                for v in values:
                    normed = _normalize_domain(v)
                    if _FILE_EXT_RE.match(normed):
                        file_like.add(normed)
                    else:
                        normed_domains.add(normed)
                if normed_domains:
                    existing = set(result.get("m_domain", []))
                    existing.update(normed_domains)
                    result["m_domain"] = sorted(existing)
                if file_like:
                    existing = set(result.get("m_file", []))
                    existing.update(file_like)
                    result["m_file"] = sorted(existing)
            elif values:
                existing = set(result.get(key, []))
                existing.update(values)
                result[key] = sorted(existing)
        return result

    DetectorFactory.seed = 0

    @staticmethod
    def langdetect(text, min_words=10, min_confidence=0.90):
        words = text.strip().split()
        if len(words) < min_words:
            return []
        try:
            return [c.lang for c in detect_langs(text) if c.prob >= min_confidence]
        except:
            return []

    async def parse(self, text, ai=False, ai_client=None):

        print(f"starting")
        start = time.perf_counter()
        parsed_text = extract_iocs_from_text(text)
        print(f"extract_iocs_from_text took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        iocs = defaultdict(set, parsed_text)
        crypto = self.crypto_parser.extract_valid_addresses(text)
        print(f"extract_valid_addresses took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        all_ioc_values = {val for vals in iocs.values() for val in vals}
        lang = self.langdetect(text)
        print(f"langdetect took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        currencies = extract_currencies(text)
        print(f"extract_currencies took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        phones, country_by_phone = extract_phone_data(text, all_ioc_values)
        print(f"extract_phone_data took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        countries = extract_countries_from_text(text)
        print(f"extract_countries_from_text took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        presidio = extract_presidio_entities(self.analyzer, text, all_ioc_values)
        presidio = {k: v for k, v in presidio.items() if k not in SKIP_ENTITIES}
        print(f"extract_presidio_entities took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        creds = extract_credentials(text)
        print(f"extract_credentials took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        tags, mentions = extract_hashtags_mentions(text)
        print(f"extract_hashtags_mentions took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        profiles, platforms_found = extract_social_profiles(text)
        print(f"extract_social_profiles took {time.perf_counter() - start:.4f} seconds")

        summary = None
        if ai and ai_client:
            start = time.perf_counter()
            summary = await ai_client.summarize_darkweb_report(
                text, model="tinyllama", force_llama32_when_summarize=True
            )
            print(f"summarize_darkweb_report took {time.perf_counter() - start:.4f} seconds")

        start = time.perf_counter()
        grouped = self.unify_entities(
            platforms_found, crypto, lang, currencies,
            profiles, phones, countries, iocs, presidio,
            creds, tags, mentions, summary
        )
        print(f"unify_entities took {time.perf_counter() - start:.4f} seconds")

        excluded = {"m_percent", "m_iocs", "m_loc", "m_work_of_art", "m_nrp", "m_in_pan", "m_bitcoin_addresses"}
        email_keys = {"m_emails", "m_iocs", "m_email_addresses", "m_email_addresses_complete"}
        merged = {}
        for k, values in grouped.items():
            if not values or k in excluded:
                continue

            def valid(val: str):
                if k in {"m_person", "m_org", "m_location"}:
                    if len(val) > 15:
                        return False
                    for ch in val:
                        if not (ch.isalnum() or ch in {'_', ' '}):
                            return False
                return True

            if k in email_keys:
                merged.setdefault("m_email", set()).update(v for v in values if v and valid(v))
                continue
            merged.setdefault(k, set()).update(v for v in values if v and valid(v))

        crypto_set = {c.lower() for c in merged.get("m_crypto_address", [])}
        stripped_crypto = {c.lower().removeprefix("0x") for c in crypto_set}

        if "m_hashes" in merged:
            cleaned = set()
            for h in merged["m_hashes"]:
                hl = h.lower()
                if hl in crypto_set:
                    continue
                if hl in stripped_crypto:
                    continue
                cleaned.add(h)
            merged["m_hashes"] = cleaned

        return [{k: v} for k, vs in merged.items() for v in vs]
