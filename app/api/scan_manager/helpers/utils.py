import os
from urllib.parse import urlparse

def unset_env():
    for k in ("HTTP_PROXY","HTTPS_PROXY","http_proxy","https_proxy","NO_PROXY","no_proxy"):
        os.environ.pop(k, None)

def eTLD_match(host: str, root: str) -> bool:
    if not host or not root:
        return False
    host = host.lower()
    root = root.lower()
    return host == root or host.endswith("." + root)

def parse_host_from_url(u: str) -> str:
    try:
        return urlparse(u).hostname or ""
    except Exception:
        return ""

def header_present(hdr_blob: str, name: str) -> bool:
    name_lc = name.lower() + ":"
    for ln in (hdr_blob or "").splitlines():
        if ln.lower().startswith(name_lc):
            return True
    return False

def headers_to_dict(hdr_blob: str) -> dict:
    out = {}
    for ln in (hdr_blob or "").splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            out[k.strip().lower()] = v.strip()
    return out

def parse_set_cookies(hdr_blob: str):
    cookies = []
    for ln in (hdr_blob or "").splitlines():
        if ln.lower().startswith("set-cookie:"):
            cookies.append(ln.split(":",1)[1].strip())
    return cookies

def categorize_alert(name: str) -> str:
    n = (name or "").lower()
    if "mixed content" in n:
        return "Mixed Content"
    if "strict-transport-security" in n or "hsts" in n:
        return "Transport"
    if "x-frame-options" in n or "anti-clickjacking" in n:
        return "Headers"
    if "x-content-type-options" in n or "nosniff" in n:
        return "Headers"
    if "referrer-policy" in n:
        return "Headers"
    if "cors" in n or "cross-domain" in n:
        return "CORS"
    if "cookie" in n or "samesite" in n or "httponly" in n or "secure flag" in n:
        return "Cookies"
    if "content security policy" in n or "csp" in n or "permissions-policy" in n or "feature-policy" in n:
        return "CSP/Policy"
    if "server" in n or "x-powered-by" in n or "banner" in n:
        return "Server Info"
    if "cache-control" in n or "cached" in n:
        return "Caching"
    if "csrf" in n:
        return "Forms"
    if "open redirect" in n:
        return "Redirects"
    if "modern web application" in n:
        return "Informational"
    return "General"
