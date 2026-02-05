import requests
import os, time, json, threading, re, socket

from datetime import datetime
from urllib.parse import urlparse, urljoin
from collections import defaultdict
from zapv2 import ZAPv2
from api.constants.constant import S_SCANNER
from api.model.scan_models import Threat, ScanMeta
from api.scan_manager.helpers.utils import categorize_alert
from api.scan_manager.helpers.zap_helpers import ZAPH
from api.scan_manager.scanners.alert_snippets import AlertSnippets
from api.scan_manager.scanners.checks_body import BodyChecks
from api.scan_manager.scanners.checks_headers import HeaderChecks
from api.scan_manager.scanners.checks_network import NetworkChecks
from api.scan_manager.scanners.pii_checks import PIIChecks
from api.scan_manager.scanners.port_scanner import port_scanner
from api.scan_manager.scanners.repository_scanner import repository_scanner
from api.scan_manager.scanners.seo_scanner import seo_scanner
from .scanners.subdomain_scanner import SubdomainScanner
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.redis_manager.redis_enums import REDIS_COMMANDS

SEC_HDR_KEYS = (
    "content-security-policy",
    "content-security-policy-report-only",
    "strict-transport-security",
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
    "permissions-policy",
    "feature-policy",
)


class domain_scanner:

    def __init__(self, zap_addr=None, api_key=None):
        self.domain_address = (zap_addr or os.environ.get("ZAP_ADDR", "http://trusted-micros-zap:8090")).rstrip("/")
        self.api_key = ("" if api_key is None else api_key) or os.environ.get("ZAP_API_KEY", "")
        self.zap = ZAPv2(apikey=self.api_key, proxies={"http": self.domain_address, "https": self.domain_address})
        self.zh = ZAPH(self.zap)
        self.port_scanner = port_scanner()
        self._mem = {}
        self.subdomain_scanner = SubdomainScanner()
        self._mem_lock = threading.Lock()
        try:
            rc = redis_controller()
            for k in rc.invoke_trigger(REDIS_COMMANDS.S_GET_KEYS):
                if isinstance(k, str) and k.startswith("scan:state:"):
                    raw = rc.invoke_trigger(REDIS_COMMANDS.S_GET_STRING, [k, None, None])
                    if raw:
                        st = json.loads(raw)
                        if st.get("status") == "pending":
                            rc.invoke_trigger(
                                REDIS_COMMANDS.S_SET_STRING,
                                [k, json.dumps({"status": "error", "result": None, "progress": 0, "step": "restarted", "scan_type": st.get("scan_type")}, ensure_ascii=False), S_SCANNER.EXPIRY_TTL],
                            )
        except Exception:
            pass

    def wait_for_zap(self, timeout: int = 60):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                v = self.zap.core.version
                if v:
                    return v
            except Exception:
                pass
            time.sleep(0.5)
        raise TimeoutError(f"ZAP not reachable at {self.domain_address}")

    def _r_set(self, key, value, ttl=None):
        try:
            rc = redis_controller()
        except Exception:
            rc = None
        if rc:
            rc.invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [key, value, ttl])
            return
        exp = (time.time() + ttl) if ttl else None
        with self._mem_lock:
            self._mem[key] = (value, exp)

    def _r_get(self, key, default=None, ttl=None):
        try:
            rc = redis_controller()
        except Exception:
            rc = None
        if rc:
            return rc.invoke_trigger(REDIS_COMMANDS.S_GET_STRING, [key, None, None])
        with self._mem_lock:
            v = self._mem.get(key)
            if not v:
                return None
            val, exp = v
            if exp is not None and exp < time.time():
                self._mem.pop(key, None)
                return None
            return val

    def _scan_keys(self, url: str, scan_type: str):
        u = self._normalize_url(url)
        p = urlparse(u)
        ident = p.netloc or u
        base = f"urlscan:{ident}:{scan_type or ''}"
        return base + ":status", base + ":result", base + ":progress", base + ":step", u

    def _set_progress(self, progress_key, step_key, progress: int, step: str, ttl=S_SCANNER.EXPIRY_TTL):
        try:
            self._r_set(progress_key, str(int(max(0, min(100, progress)))), ttl)
            self._r_set(step_key, step, ttl)
        except Exception:
            pass

    def _emit_state(self, state_key: str, url_for_keys: str, status: str, progress: int, step: str, scan_type: str, result=None, ttl=S_SCANNER.EXPIRY_TTL):
        payload = {"status": status, "result": result, "progress": int(max(0, min(100, progress))), "step": step, "scan_type": scan_type}
        self._r_set(state_key, json.dumps(payload), ttl)
        s_key, r_key, p_key, st_key, _ = self._scan_keys(url_for_keys, scan_type)
        try:
            self._r_set(s_key, status, ttl)
            self._r_set(p_key, str(payload["progress"]), ttl)
            self._r_set(st_key, step, ttl)
            if result is not None:
                self._r_set(r_key, json.dumps(result), ttl)
        except Exception:
            pass

    @staticmethod
    def _status_code_from_header(h):
        try:
            line = (h or "").splitlines()[0]
            parts = line.split()
            for p in parts:
                if p.isdigit() and len(p) == 3:
                    return int(p)
        except Exception:
            pass
        return None

    @staticmethod
    def _header_value(h, name):
        name_lc = name.lower() + ":"
        for ln in (h or "").splitlines():
            if ln.lower().startswith(name_lc):
                return ln.split(":", 1)[1].strip()
        return ""

    @staticmethod
    def _has_header(h: str, name: str) -> bool:
        pat = re.compile(rf"^\s*{re.escape(name)}\s*:", re.IGNORECASE | re.MULTILINE)
        return bool(pat.search(h or ""))

    @staticmethod
    def _get_header_values(h: str, name: str):
        pat = re.compile(rf"^\s*{re.escape(name)}\s*:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
        return [m.group(1).strip() for m in pat.finditer(h or "")]

    @staticmethod
    def _normalize_url(u: str) -> str:
        s = (u or "").strip()
        if s.lower().startswith("http:/") and not s.lower().startswith("http://"):
            s = "http://" + s.split("http:/", 1)[1].lstrip("/")
        if s.lower().startswith("https:/") and not s.lower().startswith("https://"):
            s = "https://" + s.split("https:/", 1)[1].lstrip("/")
        if not s.lower().startswith(("http://", "https://")):
            s = "https://" + s.lstrip("/")
        p = urlparse(s)
        netloc = p.netloc or p.path.split("/", 1)[0]
        rest = (p.path if p.netloc else ("/" + p.path.split("/", 1)[1] if "/" in p.path else ""))
        keep_path_hosts = ("github.com", "gitlab.com", "bitbucket.org",
                           "sourceforge.net", "gitea.com", "codeberg.org", "dev.azure.com")
        host = netloc.lower()
        if host.startswith("www.") and host[4:] in keep_path_hosts:
            netloc = netloc[4:]
            host = host[4:]
        elif host not in keep_path_hosts and not host.startswith("www."):
            netloc = "www." + netloc
            host = netloc.lower()
        if host in keep_path_hosts:
            if p.query:
                rest += "?" + p.query
            if p.fragment:
                rest += "#" + p.fragment
        else:
            rest = ""
        s = f"https://{netloc}{rest}"
        return s

    def _access_with_redirects(self, url, max_hops=10):
        current = url
        res_hdr = ""
        res_body = ""
        for _ in range(max_hops):
            h, b = self.zh.access_with_follow(current)
            res_hdr, res_body = h, b
            status = self._status_code_from_header(res_hdr)
            if status and 300 <= status < 400:
                loc = self._header_value(res_hdr, "location")
                if not loc:
                    break
                nxt = urljoin(current, loc)
                current = nxt
                time.sleep(0.1)
                continue
            break
        return current, res_hdr, res_body

    @staticmethod
    def _looks_like_incomplete_headers(h: str) -> bool:
        if not h or len(h) < 12:
            return True
        if "\n" not in h and "\r" not in h:
            return True
        lc = h.lower()
        if not any(k in lc for k in SEC_HDR_KEYS):
            return True
        return False

    def _best_history_headers_for(self, baseurl: str, final_url: str) -> str:
        try:
            try:
                msgs = self.zap.core.messages(baseurl=baseurl, start=0, count=50)
            except Exception:
                msgs = self.zap.core.messages(baseurl=baseurl)
        except Exception:
            return ""
        if not msgs:
            return ""
        best = ""
        best_score = -1
        f = urlparse(final_url)
        fhost = (f.hostname or "").lower()
        fpath = f.path or "/"
        for m in msgs:
            rh = (m.get("responseHeader") or "").strip()
            if not rh:
                continue
            reqh = (m.get("requestHeader") or "")
            status = self._status_code_from_header(rh)
            is_terminal = bool(status and status >= 200 and status < 300)
            score = 0
            if fhost and fhost in reqh.lower():
                score += 3
            if fpath and fpath in reqh:
                score += 1
            if is_terminal:
                score += 3
            lcrh = rh.lower()
            for k in SEC_HDR_KEYS:
                if k in lcrh:
                    score += 1
            if score > best_score:
                best = rh
                best_score = score
        return best

    def _requests_headers(self, final_url: str) -> str:
        try:
            proxies = {"http": self.domain_address, "https": self.domain_address}
            headers = {"User-Agent": "Mozilla/5.0 (compatible; OrionScanner/1.0)"}
            resp = requests.get(final_url, headers=headers, proxies=proxies, timeout=20, allow_redirects=True, verify=False, stream=True)
            http_ver = "HTTP/1.1"
            try:
                ver = getattr(resp.raw, "version", 11)
                if ver == 10:
                    http_ver = "HTTP/1.0"
                elif ver == 11:
                    http_ver = "HTTP/1.1"
                elif ver == 20:
                    http_ver = "HTTP/2"
            except Exception:
                pass
            status_line = f"{http_ver} {resp.status_code} {resp.reason or ''}".strip()
            lines = [status_line]
            for k, v in resp.headers.items():
                lines.append(f"{k}: {v}")
            return "\r\n".join(lines) + "\r\n"
        except Exception:
            return ""

    def _cache_key(self, url: str, scan_type: str) -> str:
        u = self._normalize_url(url)
        p = urlparse(u)
        keep_path_hosts = ("github.com", "gitlab.com", "bitbucket.org",
                           "sourceforge.net", "gitea.com", "codeberg.org", "dev.azure.com")
        ident = p.netloc
        if any(h in p.netloc.lower() for h in keep_path_hosts):
            ident += p.path.rstrip("/")
        return f"scan:cache:{scan_type}:{ident}"

    def _get_cached(self, key: str):
        try:
            raw = self._r_get(key)
            return json.loads(raw) if raw else None
        except Exception:
            return None

    def _set_cached(self, key: str, value, ttl=S_SCANNER.EXPIRY_TTL):
        try:
            self._r_set(key, json.dumps(value, ensure_ascii=False), ttl)
        except Exception:
            pass

    def scan(self, target_url, scan_type, scanner_name="Orion Intelligence", progress_cb=None, check_live=False):
        if scan_type == "subdomains":
            parsed = urlparse(target_url if "://" in target_url else f"https://{target_url}")
            root = (parsed.hostname or target_url).lstrip("www.")
            cache_key = self._cache_key(root, scan_type)
        else:
            cache_key = self._cache_key(target_url, scan_type)

        if getattr(S_SCANNER, "ENABLE_SCAN_CACHE", False) or scan_type=="seo" or scan_type=="repo":
            cached = self._get_cached(cache_key)
            if cached:
                if progress_cb: progress_cb(100, "cache_hit")
                return cached

        if scan_type == "repo":
            try:
                res = repository_scanner().parse(target_url, progress_cb=progress_cb)
                self._set_cached(cache_key, res)
                return res
            except Exception as _:
                return {"status": "error", "result": None, "progress": 0, "step": "error"}

        if scan_type == "seo":
            try:
                res = seo_scanner().parse(target_url, progress_cb=progress_cb)
                self._set_cached(cache_key, res)
                return res
            except Exception as _:
                return {"status": "error", "result": None, "progress": 0, "step": "error"}

        if scan_type == "subdomains":
            parsed = urlparse(target_url if "://" in target_url else f"https://{target_url}")
            domain = parsed.hostname or target_url
            domain = domain.lstrip("www.")

            if not domain:
                return {"status": "error", "message": "Invalid domain", "subdomains": []}

            result = self.subdomain_scanner.scan(domain, progress_cb=progress_cb,check_live=check_live)

            final = {
                "meta": {
                    "URL": target_url,
                    "Host": domain,
                    "Scanned_on_date": datetime.now().strftime("%B %d, %Y"),
                    "Scanned_by": scanner_name
                },
                "subdomains": result["subdomains"],
                "count": result["count"],
                "status": result["status"],
                "message": result.get("message", "")
            }
            if "live_subdomains" in result:
                final["live_subdomains"] = result["live_subdomains"]
                final["live_count"] = result["live_count"]

            return final

        if progress_cb:
            progress_cb(5, "resolving")
        target_url = self._normalize_url(target_url)
        p = urlparse(target_url)
        if not p.hostname:
            if progress_cb: progress_cb(0, "error")
            return {"status": "error", "result": None, "progress": 0, "step": "error"}
        try:
            socket.getaddrinfo(p.hostname, None)
        except Exception:
            if progress_cb: progress_cb(0, "error")
            return {"status": "error", "result": None, "progress": 0, "step": "error"}
        if progress_cb:
            progress_cb(10, "requesting")
        try:
            final_url, res_hdr, res_body = self._access_with_redirects(target_url)
        except Exception:
            if progress_cb: progress_cb(0, "error")
            return {"status": "error", "result": None, "progress": 0, "step": "error"}
        parsed = urlparse(final_url)
        baseurl = f"{parsed.scheme}://{parsed.hostname or ''}" + (f":{parsed.port}" if parsed.port else "")
        parsed_host = parsed.hostname or ""
        if self._looks_like_incomplete_headers(res_hdr):
            req_hdr = self._requests_headers(final_url)
            if not self._looks_like_incomplete_headers(req_hdr):
                res_hdr = req_hdr
        if self._looks_like_incomplete_headers(res_hdr):
            hist_hdr = self._best_history_headers_for(baseurl, final_url)
            if not self._looks_like_incomplete_headers(hist_hdr):
                res_hdr = hist_hdr
        grouped = defaultdict(list)
        grouped_proofs = defaultdict(list)

        def add(category, header, description, confidence, risk):
            grouped[category].append(Threat(header=header, description=description, confidence=confidence, risk=risk))

        if progress_cb:
            progress_cb(20, "header_checks")
        if res_hdr:
            HeaderChecks.check(res_hdr, add)
        if progress_cb:
            progress_cb(50, "body_checks")
        if res_body:
            BodyChecks.mixed_content(final_url, res_body, add)
            BodyChecks.directory_listing(res_body, add)
            BodyChecks.default_index(res_body, add)
            BodyChecks.content_type_mismatch(res_hdr, res_body, add)
            BodyChecks.verbose_errors(res_body, add)
            BodyChecks.internal_indicators(res_body, add)
            BodyChecks.email_and_secrets(res_body, add)
            BodyChecks.inline_js(res_body, add)
            BodyChecks.response_size(res_body, add)
        if res_hdr:
            cc = self._header_value(res_hdr, "cache-control")
            v = (cc or "").lower()
            if (not cc) or ("public" in v and "no-store" not in v and "private" not in v) or ("max-age" not in v and "no-store" not in v and "no-cache" not in v):
                add("Caching Findings", "Re-examine Cache-control Directives", "The cache-control header has not been set properly or is missing.", "Low", "Informational")
        if res_body:
            lb = res_body.lower()
            if ("<script type=\"module\"" in lb) or ("react" in lb and "root" in lb) or ("angular" in lb) or ("vue" in lb) or ("svelte" in lb) or ("next" in lb) or ("import(" in lb) or ("fetch(" in lb) or ("webpack" in lb) or ("vite" in lb):
                add("Informational Findings", "Modern Web Application", "Modern web application detected.", "Medium", "Informational")
        if progress_cb:
            progress_cb(65, "network_checks")
        if parsed.scheme == "https" and parsed_host:
            NetworkChecks.tls_certificate(parsed_host, add, port=parsed.port or 443)
        PIIChecks.check(res_hdr or "", res_body or "", add)
        if scan_type == "advanced" and parsed_host:
            self.port_scanner.scan(parsed_host, add_cb=add, progress_cb=progress_cb, start=75, end=90)
            if progress_cb:
                progress_cb(85, "port_scan")
        if progress_cb:
            progress_cb(80, "zap_alerts")
        alerts = self.zh.alerts(baseurl)
        for a in alerts:
            cat = categorize_alert(a.get("alert", ""))
            desc = a.get("description", "") or ""
            grouped[cat].append(Threat(header=a.get("alert", "") or "", description=desc, confidence=a.get("confidence", "") or "", risk=a.get("risk", "") or ""))
        for a in alerts:
            cat = categorize_alert(a.get("alert", ""))
            chunk = AlertSnippets.augment(self.zap, baseurl, a)
            if chunk:
                grouped_proofs[cat].append({"header": a.get("alert", "") or "", "proof": chunk, "confidence": a.get("confidence", "") or "", "risk": a.get("risk", "") or ""})
        if progress_cb:
            progress_cb(90, "policy_checks")
        if res_hdr and not any(cat == "CSP/Policy" and any(t.header.lower().startswith(("content-security-policy", "permissions-policy", "feature-policy")) for t in lst) for cat, lst in grouped.items()):
            has_csp = self._has_header(res_hdr, "Content-Security-Policy")
            has_csp_ro = self._has_header(res_hdr, "Content-Security-Policy-Report-Only")
            has_pp = self._has_header(res_hdr, "Permissions-Policy") or self._has_header(res_hdr, "Feature-Policy")
            if not has_csp and not has_csp_ro:
                grouped["CSP/Policy"].append(Threat(header="Content-Security-Policy", description="CSP header missing", confidence="High", risk="Medium"))
            if has_csp_ro and not has_csp:
                vals = "; ".join(self._get_header_values(res_hdr, "Content-Security-Policy-Report-Only"))
                grouped["CSP/Policy"].append(Threat(header="Content-Security-Policy-Report-Only", description=f"CSP report-only ({vals})", confidence="High", risk="Low"))
            if not has_pp:
                grouped["CSP/Policy"].append(Threat(header="Permissions-Policy", description="Permissions-Policy header missing", confidence="High", risk="Medium"))
            if not self._has_header(res_hdr, "X-Frame-Options"):
                grouped["CSP/Policy"].append(Threat(header="X-Frame-Options", description="X-Frame-Options header missing", confidence="High", risk="Low"))
            if not self._has_header(res_hdr, "X-Content-Type-Options"):
                grouped["CSP/Policy"].append(Threat(header="X-Content-Type-Options", description="X-Content-Type-Options header missing", confidence="High", risk="Low"))
            if not self._has_header(res_hdr, "Referrer-Policy"):
                grouped["CSP/Policy"].append(Threat(header="Referrer-Policy", description="Referrer-Policy header missing", confidence="High", risk="Low"))
            if not self._has_header(res_hdr, "Strict-Transport-Security") and parsed.scheme == "https":
                grouped["CSP/Policy"].append(Threat(header="Strict-Transport-Security", description="HSTS header missing", confidence="High", risk="Medium"))
        if progress_cb:
            progress_cb(95, "finalizing")
        meta = ScanMeta(URL=final_url, Host=parsed_host, Port=("443 SSL" if parsed.scheme == "https" else "80"), Scanned_on_date=datetime.now().strftime("%B %d, %Y"), Scanned_by=scanner_name)
        summary = {k: len(v) for k, v in grouped.items()}
        high_count = medium_count = low_count = info_count = 0
        for lst in grouped.values():
            for t in lst:
                r = (t.risk or "").lower()
                if r == "high":
                    high_count += 1
                elif r == "medium":
                    medium_count += 1
                elif r == "low":
                    low_count += 1
                elif r == "informational":
                    info_count += 1
        if high_count > 0:
            grade = "F"
        elif medium_count >= 5:
            grade = "D"
        elif medium_count >= 1:
            grade = "C"
        elif low_count > 0:
            grade = "B"
        else:
            grade = "A"
        result = {
            "meta": {"URL": meta.URL, "Host": meta.Host, "Port": meta.Port, "Scanned_on_date": meta.Scanned_on_date, "Scanned_by": meta.Scanned_by},
            "summary": summary,
            "threats": {k: [t.__dict__ for t in v] for k, v in grouped.items()},
            "proofs": dict(grouped_proofs),
            "grade": grade,
            "grade_counts": {"high": high_count, "medium": medium_count, "low": low_count, "informational": info_count},
        }
        if getattr(S_SCANNER, "ENABLE_SCAN_CACHE", False):
            self._set_cached(cache_key, result)
        if progress_cb:
            progress_cb(100, "complete")
        return result

    def run_scan(self, url, scan_type,check_live=False):
        state_key, normalized = self._scan_state_key(url, scan_type)
        self._emit_state(state_key, normalized, "pending", 0, "queued", scan_type)

        def cb(pct, step):
            self._emit_state(state_key, normalized, "pending", int(pct), step, scan_type)

        try:
            input_target = url if scan_type == "subdomains" else normalized
            result = self.scan(input_target, scan_type, progress_cb=cb,check_live=check_live)

            self._emit_state(state_key, normalized, "done", 100, "complete", scan_type, result=result)
            return result
        except Exception as e:
            self._emit_state(state_key, normalized, "error", 0, "error", scan_type, result=None)
            raise e

    def _scan_state_key(self, url, scan_type):
        u = self._normalize_url(url)
        p = urlparse(u)
        ident = p.netloc or u
        return f"scan:state:{ident}:{scan_type or ''}", u

    def get_scan_status(self, url, requested_type=None):
        state_key, normalized = self._scan_state_key(url, requested_type or "")
        raw = self._r_get(state_key)
        state = json.loads(raw) if raw else {}
        status = state.get("status")
        progress = state.get("progress")
        step = state.get("step")

        if status == "done":
            if not S_SCANNER.ENABLE_SCAN_CACHE:
                try:
                    rc = redis_controller()
                except Exception:
                    rc = None
                if rc:
                    rc.invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [state_key, json.dumps({}, ensure_ascii=False), 1])

            if state.get("scan_type") == "basic" and requested_type == "advanced" and not state.get("upgrade_in_progress"):
                new_state = {"status": "pending", "result": None, "progress": 0, "step": "queued_upgrade", "scan_type": "advanced", "upgrade_in_progress": True}
                self._r_set(state_key, json.dumps(new_state, ensure_ascii=False), S_SCANNER.EXPIRY_TTL)
                s_key, r_key, p_key, st_key, _ = self._scan_keys(normalized, requested_type or "")
                self._r_set(s_key, "pending", S_SCANNER.EXPIRY_TTL)
                self._r_set(p_key, "0", S_SCANNER.EXPIRY_TTL)
                self._r_set(st_key, "queued_upgrade", S_SCANNER.EXPIRY_TTL)
                return {"status": "none", "result": None, "progress": 0, "step": ""}

            return {
                "status": "done",
                "result": state.get("result"),
                "progress": int(progress or 100),
                "step": step or "complete",
            }
        if status == "pending":
            return {"status": "pending", "result": None, "progress": int(progress or 0), "step": step or ""}
        if status == "error":
            return {"status": "error", "result": None, "progress": int(progress or 0), "step": step or "error"}
        return {"status": "none", "result": None, "progress": 0, "step": ""}
