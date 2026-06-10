import os
from ddgs import DDGS
from typing import Dict, Any, Optional
from datetime import datetime, timezone

class DuckDuckGoDorker:
    def __init__(self):
        self.timestamp = datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _get_tor_proxy() -> str:

        return (
                os.getenv("TOR_IMAGE_PROXY_URL")
                or os.getenv("TOR_PROXY_URL")
                or "socks5h://trusted-social_tor_instace_1:9552"
        )

    def smart_search(self, query: str, platform: Optional[str] = None) -> Dict[str, Any]:
        platform_clean = platform.lower().strip() if platform else ""
        query_clean = query.strip()


        if platform_clean:
            dorks = [
                f'site:{platform_clean}.com "{query_clean}"',
                f'inurl:{platform_clean} "{query_clean}"',
                f'{query_clean} {platform_clean} profile'
            ]
        else:
            dorks = [
                f'"{query_clean}" social profile',
                f'"{query_clean}" contact OR portfolio'
            ]

        results_list = []
        seen_urls = set()
        proxy = self._get_tor_proxy()

        print(f"[DuckDuckGoDorker] Starting search for '{query_clean}' on '{platform_clean}'")

        for dork in dorks:
            print(f"[*] Executing Dork: {dork}")
            search_results = []


            try:
                print(f"[+] Trying via Tor Proxy...")
                with DDGS(proxy=proxy) as ddgs:

                    search_results = list(ddgs.text(dork, max_results=10))
            except Exception as proxy_error:
                print(f"[-] Tor Proxy Failed: {proxy_error}")
                print(f"[+] Switching to Direct Connection for this dork...")

                try:
                    with DDGS() as ddgs:
                        search_results = list(ddgs.text(dork, max_results=10))
                except Exception as direct_error:
                    print(f"[-] Direct Search also failed: {direct_error}")
                    continue

            if not search_results:
                print(f"[-] No results for dork: {dork}. Moving to next...")
                continue

            for r in search_results:
                url = r.get("href", "")
                if not url or url in seen_urls:
                    continue

                if platform_clean and platform_clean not in url.lower():
                    continue

                seen_urls.add(url)
                results_list.append({
                    "title": r.get("title", ""),
                    "url": url,
                    "snippet": r.get("body", ""),
                    "found_via_dork": dork
                })

            if len(results_list) >= 3:
                break

        return {
            "query": query_clean,
            "platform": platform_clean or "All",
            "total_found": len(results_list),
            "timestamp": self.timestamp,
            "results": results_list
        }