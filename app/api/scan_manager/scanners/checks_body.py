
import re

class BodyChecks:
    @staticmethod
    def mixed_content(final_url, res_body, add):
        if final_url.lower().startswith("https://") and "http://" in (res_body or ""):
            add("Mixed Content","Insecure subresources","Page contains 'http://' references on HTTPS page","Medium","Medium")

    @staticmethod
    def directory_listing(res_body, add):
        if "Index of /" in (res_body or ""):
            add("Directory Listing","Index of /","Directory listing appears enabled","High","Medium")

    @staticmethod
    def default_index(res_body, add):
        markers = ["Apache2 Ubuntu Default Page","Welcome to nginx!","IIS Windows Server","Test Page for the Nginx HTTP Server"]
        body = res_body or ""
        for m in markers:
            if m in body:
                add("Default Page", m, "Default server page detected; may indicate misconfiguration","High","Medium")
                break

    @staticmethod
    def content_type_mismatch(res_hdr, res_body, add):
        ctype = ""
        for ln in (res_hdr or "").splitlines():
            if ln.lower().startswith("content-type:"):
                ctype = ln.split(":",1)[1].strip().lower()
                break
        body = (res_body or "").strip()
        looks_json = body.startswith("{") or body.startswith("[")
        looks_xml = body.startswith("<") and ("<?xml" in body or "<rss" in body or "<feed" in body)
        if "text/html" in ctype and (looks_json or looks_xml):
            add("Content-Type","Mismatch","Body appears JSON/XML but Content-Type is text/html","Medium","Low")

    @staticmethod
    def verbose_errors(res_body, add):
        patterns = [r"Exception in thread", r"Traceback \(most recent call last\)", r"Stacktrace:", r"SQLException", r"Fatal error:", r"NullReferenceException"]
        for pat in patterns:
            if re.search(pat, res_body or "", flags=re.I):
                add("Error Disclosure","Verbose error page",f"Body contains error pattern: {pat}","High","Medium")
                break

    @staticmethod
    def internal_indicators(res_body, add):
        b = res_body or ""
        if re.search(r"\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})\b", b):
            add("Information Disclosure","Private IP","Response appears to contain internal IP addresses","Medium","Low")

    @staticmethod
    def email_and_secrets(res_body, add):
        b = res_body or ""
        if len(re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", b, flags=re.I)) >= 3:
            add("PII","Email addresses","Multiple email addresses found in response","Medium","Low")
        if re.search(r"AKIA[0-9A-Z]{16}", b) or re.search(r"AIza[0-9A-Za-z\-_]{35}", b) or re.search(r"-----BEGIN (RSA|EC) PRIVATE KEY-----", b):
            add("Secrets","Potential secret","Key-like material present","High","High")

    @staticmethod
    def inline_js(res_body, add):
        b = res_body or ""
        if re.search(r"\son\w+\s*=", b, flags=re.I) or re.search(r"href\s*=\s*[\"']\s*javascript:", b, flags=re.I):
            add("XSS Surface","Inline JS handlers","Inline event handlers or javascript: URLs present","Medium","Low")

    @staticmethod
    def response_size(res_body, add):
        if res_body is not None and len(res_body.encode("utf-8", errors="ignore")) > 1024*1024:
            add("Anomaly","Large response","Response size exceeds 1MB; review for data exposure","Low","Low")
