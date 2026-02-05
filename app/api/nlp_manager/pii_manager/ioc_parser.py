import re, os, math, inspect
import iocextract, ioc_finder
from collections import defaultdict


class _IOCParser:
    FILE_EXT_BLOCKLIST = {
        "zip", "exe", "dll", "txt", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "iso", "dmg", "msi", "msix", "apk", "jar",
        "gz", "tgz", "bz2", "xz", "7z", "rar", "tar", "csv", "json", "xml", "yaml", "yml", "js", "css", "map", "ico", "png", "jpg",
        "jpeg", "gif", "webp", "svg", "bmp", "ps1", "bat", "sh", "py", "rb", "php", "asp", "aspx", "jsp"
    }

    HEXLEN = {
        "MD5S": 32, "MD5_HASHES": 32,
        "SHA1S": 40, "SHA1_HASHES": 40,
        "SHA256S": 64, "SHA256_HASHES": 64,
        "SHA512S": 128, "SHA512_HASHES": 128,
        "IMPHASHES": 32, "AUTHENTIHASHES": 40
    }

    ENTROPY_MIN = {32: 2.6, 40: 3.0, 64: 3.5, 128: 4.0}

    MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    EXT_RE = re.compile(r"\.[A-Za-z0-9]{1,6}$")

    KNOWN_DOMAIN_TOKENS = {
        ".com", ".net", ".org", ".edu", ".gov", ".mil", ".int", ".io", ".co", ".info", ".biz",
        ".online", ".site", ".app", ".dev", ".ai", ".gg", ".me", ".us", ".uk", ".de", ".jp", ".cn",
        ".ru", ".xyz", ".pro", ".tv", ".in", ".pk", ".rock"
    }

    SKIP_FUNCS = {
        "parse_google_analytics_ids",
        "parse_google_adsense_ids",
        "parse_bitcoin_addresses",
        "parse_complete_email_addresses",
        "parse_tlp_labels",
    }

    SKIP_KEYS = {
        "GOOGLE_ANALYTICS_IDS",
        "GOOGLE_ADSENSE_IDS",
        "BITCOIN_ADDRESSES",
        "COMPLETE_EMAIL_ADDRESSES",
    }

    def __init__(self):
        self.parse_funcs = self._load_parse_funcs()
        self.extract_funcs = self._load_extract_funcs()

    @staticmethod
    def _entropy(x: str) -> float:
        if not x:
            return 0.0
        m = len(x)
        freq = {}
        for c in x:
            freq[c] = freq.get(c, 0) + 1
        return -sum((v / m) * math.log2(v / m) for v in freq.values())

    @staticmethod
    def _is_low_variation(x: str) -> bool:
        return bool(
            re.fullmatch(r"([0-9a-fA-F])\1+", x) or
            re.fullmatch(r"([0-9a-fA-F]{2})\1+", x)
        )

    def _hex_ok(self, x: str, n: int) -> bool:
        return len(x) == n and re.fullmatch(rf"[0-9a-fA-F]{{{n}}}", x) is not None

    def _filter_hash_bucket(self, label: str, vals):
        n = self.HEXLEN.get(label)
        if not n:
            return sorted(set(vals))
        out = set()
        for v in vals:
            hv = v.strip()
            if not self._hex_ok(hv, n):
                continue
            if self._is_low_variation(hv):
                continue
            if self._entropy(hv) < self.ENTROPY_MIN.get(n, 2.5):
                continue
            out.add(hv)
        return sorted(out)

    def _normalize_domain(self, candidate: str):
        d = candidate.strip().lower()
        if not d:
            return None
        url_like = d.startswith(("http://", "https://", "www.", "//"))
        if not url_like and not any(t in d for t in self.KNOWN_DOMAIN_TOKENS):
            return None
        n = d
        if url_like:
            if n.startswith("http://"):
                n = n[7:]
            elif n.startswith("https://"):
                n = n[8:]
            elif n.startswith("//"):
                n = n[2:]
            if n.startswith("www."):
                n = n[4:]
            for sep in ("/", "?", "#"):
                if sep in n:
                    n = n.split(sep, 1)[0]
        if "@" in n:
            n = n.split("@", 1)[-1]
        if ":" in n:
            n = n.split(":", 1)[0]
        n = n.strip(".")
        if not n or "." not in n:
            return None
        tld = n.rsplit(".", 1)[-1]
        if not tld.isalpha():
            return None
        if tld in self.FILE_EXT_BLOCKLIST:
            return None
        return n

    def _domains_from_urls(self, vals):
        s = set()
        for v in vals:
            nd = self._normalize_domain(v)
            if nd:
                s.add(nd)
        return s

    def _filter_file_paths(self, vals):
        s = set()
        for raw in vals:
            if not raw:
                continue
            for p in re.split(r"[,\s]+", str(raw).strip()):
                p = p.strip(" \t\r\n'\"<>[]()")
                if not p:
                    continue
                name = os.path.basename(p)
                if not name:
                    continue
                if name.endswith("."):
                    continue
                _, ext = os.path.splitext(name)
                if not ext:
                    continue
                if not self.EXT_RE.fullmatch(ext):
                    continue
                s.add(p)
        return s

    def _load_parse_funcs(self):
        out = []
        for n, f in inspect.getmembers(ioc_finder, inspect.isfunction):
            if not n.startswith("parse_") or n in self.SKIP_FUNCS:
                continue

            k = n[6:].upper()
            if not k.endswith("S"):
                k += "S"
            out.append((k, f))
        return out

    @staticmethod
    def _load_extract_funcs():
        out = []
        for n, f in inspect.getmembers(iocextract, inspect.isfunction):
            if not n.startswith("extract_"):
                continue
            k = n[8:].upper()
            has_refang = "refang" in inspect.signature(f).parameters
            out.append((k, f, has_refang))
        return out

    def _run_iocextract(self, text: str):
        a = defaultdict(set)
        for k, f, has_refang in self.extract_funcs:
            try:
                r = f(text, refang=True) if has_refang else f(text)
                if k in {"URLS", "UNENCODED_URLS"}:
                    a["DOMAINS"] |= self._domains_from_urls(r)
                elif "DOMAIN" in k:
                    for v in r:
                        nd = self._normalize_domain(v)
                        if nd and any(nd.endswith(t) for t in self.KNOWN_DOMAIN_TOKENS):
                            a["DOMAINS"].add(nd)
                else:
                    for v in r:
                        a[k].add(v)
            except Exception:
                pass
        return a

    def _run_ioc_finder(self, text: str):
        b = defaultdict(set)
        if len(text) >= 500000:
            return b
        try:
            t = ioc_finder.prepare_text(text)
        except Exception:
            t = text
        for k, f in self.parse_funcs:
            if k in self.SKIP_KEYS:
                continue
            try:
                r = f(t) or []
                if k in {"URLS", "UNENCODED_URLS"}:
                    b["DOMAINS"] |= self._domains_from_urls(r)
                elif "DOMAIN" in k:
                    for v in r:
                        nd = self._normalize_domain(v)
                        if nd and any(nd.endswith(t) for t in self.KNOWN_DOMAIN_TOKENS):
                            b["DOMAINS"].add(nd)
                elif k == "FILE_PATHS":
                    for v in r:
                        ext = os.path.splitext(v)[1][1:].lower()
                        if ext in self.FILE_EXT_BLOCKLIST:
                            b[k].add(v)
                else:
                    for v in r:
                        b[k].add(v)
            except Exception:
                pass
        return b

    def _postprocess(self, union: dict):
        union.pop("URLS", None)
        union.pop("UNENCODED_URLS", None)
        union["DOMAINS"] = sorted(
            set(self._domains_from_urls(union.get("URLS", []))) |
            set(self._domains_from_urls(union.get("UNENCODED_URLS", []))) |
            {d for d in union.get("DOMAINS", []) if self._normalize_domain(d)}
        )

        union = {
            k: v for k, v in union.items()
            if k.upper() not in {"IOC", "IOCS", "TELEPHONE_NUMS", "GPE"}
               and "BITCOIN" not in k.upper()
               and "BTC" not in k.upper()
        }

        if "FILE_PATHS" in union:
            union["FILE_PATHS"] = sorted(self._filter_file_paths(union["FILE_PATHS"]))

        for lbl in list(union.keys()):
            if lbl in self.HEXLEN:
                union[lbl] = self._filter_hash_bucket(lbl, union[lbl])

        if "HASHES" in union:
            mixed = []
            for x in union["HASHES"]:
                xl = len(x)
                for lbl, need in self.HEXLEN.items():
                    if xl == need and re.fullmatch(rf"[0-9a-fA-F]{{{need}}}", x):
                        mixed.append(x)
                        break
            union["HASHES"] = sorted({
                h for h in mixed
                if not self._is_low_variation(h) and self._entropy(h) >= self.ENTROPY_MIN.get(len(h), 2.5)
            })

        for k in ("IPS", "IPV4S", "IPV6S"):
            if k in union:
                real, macs = [], []
                for v in union[k]:
                    if self.MAC_RE.fullmatch(v):
                        macs.append(v)
                    else:
                        real.append(v)
                union[k] = real
                if macs:
                    union["MAC_ADDRESSES"] = sorted(set(union.get("MAC_ADDRESSES", [])) | set(macs))

        union.pop("IPS", None)
        union.pop("IPV4S", None)
        union.pop("IPV6S", None)

        return union

    def parse(self, text: str) -> dict:
        a = self._run_iocextract(text)
        b = self._run_ioc_finder(text)

        a = {k: sorted(v) for k, v in a.items()}
        b = {k: sorted(v) for k, v in b.items()}

        keys = set(a) | set(b)
        out = {}

        for k in keys:
            if k == "EMAILS":
                aset = {x.lower(): x for x in a.get(k, [])}
                bset = {x.lower(): x for x in b.get(k, [])}
                inter_lc = set(aset.keys()) & set(bset.keys())
                out[k] = sorted({aset.get(x) or bset.get(x) for x in inter_lc})

            elif k in {"MD5S", "MD5_HASHES", "SHA1S", "SHA1_HASHES",
                       "SHA256S", "SHA256_HASHES", "SHA512S", "SHA512_HASHES"}:
                aset = set(a.get(k, []))
                bset = set(b.get(k, []))
                inter = aset & bset
                out[k] = sorted(inter)

            else:
                out[k] = sorted(set(a.get(k, [])) | set(b.get(k, [])))

        all_hashes = set()
        for lbl in ("MD5S", "MD5_HASHES", "SHA1S", "SHA1_HASHES",
                    "SHA256S", "SHA256_HASHES", "SHA512S", "SHA512_HASHES"):
            all_hashes |= set(out.get(lbl, []))
        if all_hashes:
            out["HASHES"] = sorted(all_hashes)

        return self._postprocess(out)
