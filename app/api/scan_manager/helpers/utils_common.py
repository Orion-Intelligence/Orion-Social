
import os

def unset_env():
    for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "NO_PROXY", "no_proxy"]:
        os.environ.pop(k, None)

def eTLD_match(a: str, b: str) -> bool:
    if not a or not b: return False
    a = a.lower().lstrip(".")
    b = b.lower().lstrip(".")
    return a == b or a.endswith("."+b) or b.endswith("."+a)

def header_present(h: str, name: str) -> bool:
    if not h or not name: return False
    name = name.lower() + ":"
    for ln in h.splitlines():
        if ln.lower().startswith(name):
            return True
    return False

def categorize_alert(alert_name: str) -> str:
    n = (alert_name or "").lower()
    if any(w in n for w in ["cookie", "session"]): return "Cookies"
    if "cors" in n: return "CORS"
    if "content security policy" in n or "csp" in n: return "CSP/Policy"
    if any(w in n for w in ["header","clickjacking","x-frame","x-content-type"]): return "Headers"
    if any(w in n for w in ["hsts","transport","ssl","tls"]): return "Transport"
    if any(w in n for w in ["server","powered-by"]): return "Server Info"
    if any(w in n for w in ["csrf","form"]): return "Forms"
    if any(w in n for w in ["pii_manager","credit","ssn","email"]): return "PII"
    if any(w in n for w in ["cache"]): return "Caching"
    return "General"

def snippet(text: str, evidence: str = "", pad: int = 160, maxlen: int = 600) -> str:
    if not text: return ""
    if evidence:
        i = text.find(evidence)
        if i >= 0:
            a = max(0, i-pad); b = min(len(text), i+len(evidence)+pad)
            s = text[a:b]
            return s if len(s) <= maxlen else s[:maxlen]
    return text[:maxlen]
