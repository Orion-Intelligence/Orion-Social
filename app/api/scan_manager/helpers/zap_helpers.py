
from urllib.parse import urljoin

class ZAPH:
    def __init__(self, zap):
        self.zap = zap

    def access_with_follow(self, url: str):
        res_hdr, res_body = "", ""
        try:
            r = self.zap.core.access_url(url=url, followredirects=True)
            if isinstance(r, dict) and r.get("accessUrl"):
                entry = r["accessUrl"][0]
                res_hdr = entry.get("responseHeader","") or ""
                res_body = entry.get("responseBody","") or ""
        except Exception:
            pass
        return res_hdr, res_body

    def fetch_path(self, baseurl: str, path: str):
        try:
            r = self.zap.core.access_url(url=urljoin(baseurl.rstrip('/')+'/', path.lstrip('/')), followredirects=True)
            if isinstance(r, dict) and r.get("accessUrl"):
                e = r["accessUrl"][0]
                return e.get("responseHeader","") or "", e.get("responseBody","") or ""
        except Exception:
            pass
        return "", ""

    def alerts(self, baseurl: str):
        try:
            return self.zap.core.alerts(baseurl=baseurl, start=0, count=10000) or []
        except Exception:
            return []

    def message_by_id(self, mid: int):
        try:
            return self.zap.core.message(int(mid))
        except Exception:
            return None
