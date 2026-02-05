import json, requests
from datetime import datetime
from fastapi import HTTPException
from urllib.parse import urlparse

from crawler.crawler_services.shared.env_handler import env_handler


class seo_scanner:
    API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    API_KEY = env_handler.get_instance().env("S_LIGHT_HOUSE_API_KEY","")

    def _scan(self, target_url):
        try:
            r = requests.get(self.API, params={"url": target_url, "key": self.API_KEY, "strategy": "desktop", "category": "seo"}, timeout=60)
            if r.status_code != 200:
                raise HTTPException(status_code=500, detail=f"HTTP {r.status_code}: {r.text[:200]}")
            d = r.json()
            lh = d.get("lighthouseResult", {})
            seo = lh.get("categories", {}).get("seo", {})
            ids = [a["id"] for a in seo.get("auditRefs", [])]
            audits = lh.get("audits", {})
            score = seo.get("score")
            pct = int(round((score or 0) * 100))
            rank = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"
            threats = {"SEO Audits": []}
            for i in ids:
                a = audits.get(i, {})
                sc = a.get("score")
                if sc is None or sc == 1:
                    continue
                threats["SEO Audits"].append({
                    "header": a.get("title"),
                    "description": a.get("description"),
                    "confidence": "High",
                    "risk": "Medium"
                })
            return lh.get("finalUrl"), score, pct, rank, threats
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"SEO scan failed for {target_url}: {str(e)}")

    def parse(self, url, scanner_name="Orion Intelligence", progress_cb=None):
        if progress_cb: progress_cb(5, "queued")
        if progress_cb: progress_cb(10, "requesting")
        final_url, score, pct, rank, threats = self._scan(url)
        if progress_cb: progress_cb(80, "processing")

        parsed = urlparse(final_url or url)
        host = parsed.hostname or ""
        port = "443 SSL" if parsed.scheme == "https" else "80"
        summary = {"SEO Audits": len(threats.get("SEO Audits", []))}
        grade_counts = {"high": 0, "medium": 0, "low": 0, "informational": 0}
        for lst in threats.values():
            for t in lst:
                r = (t["risk"] or "").lower()
                if r == "high": grade_counts["high"] += 1
                elif r == "medium": grade_counts["medium"] += 1
                elif r == "low": grade_counts["low"] += 1
                elif r == "informational": grade_counts["informational"] += 1

        result = {
            "meta": {
                "URL": final_url,
                "Host": host,
                "Port": port,
                "Scanned_on_date": datetime.now().strftime("%B %d, %Y"),
                "Scanned_by": scanner_name
            },
            "summary": summary,
            "threats": threats,
            "proofs": {},
            "grade": rank,
            "grade_counts": grade_counts
        }

        with open("seo_report.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        if progress_cb: progress_cb(100, "complete")
        return result

if __name__ == "__main__":
    seo_scanner().parse("https://bbc.com/")
