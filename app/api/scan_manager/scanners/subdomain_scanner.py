import subprocess
import json
import httpx
import asyncio
from typing import List, Dict, Optional


class SubdomainScanner:

    def __init__(self):
        pass

    async def _check_live_domain(self, client: httpx.AsyncClient, subdomain: str) -> Optional[str]:

        for scheme in ['https', 'http']:
            url = f"{scheme}://{subdomain}"
            try:
                response = await client.get(url, follow_redirects=True)
                if response.status_code:
                    return subdomain
            except (httpx.ConnectError, httpx.TimeoutException, httpx.TooManyRedirects):
                continue
            except Exception:
                continue

        return None

    async def _check_domains_live_async(self, subdomains: List[str], progress_cb=None) -> List[str]:
        live_subdomains = []
        total = len(subdomains)
        processed = 0

        async with httpx.AsyncClient(
                timeout=httpx.Timeout(5.0, connect=3.0),
                verify=False,
                follow_redirects=True,
                limits=httpx.Limits(max_connections=50, max_keepalive_connections=20),
                headers={'User-Agent': 'Mozilla/5.0 (compatible; OrionScanner/1.0)'}
        ) as client:

            tasks = [self._check_live_domain(client, subdomain) for subdomain in subdomains]

            for coro in asyncio.as_completed(tasks):
                processed += 1
                try:
                    result = await coro
                    if result:
                        live_subdomains.append(result)

                    if progress_cb and total > 0:
                        progress = 75 + int((processed / total) * 20)
                        progress_cb(progress, f"checking_live ({processed}/{total})")
                except Exception:
                    pass

        return sorted(live_subdomains)

    def _check_domains_live(self, subdomains: List[str], progress_cb=None) -> List[str]:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(
                self._check_domains_live_async(subdomains, progress_cb)
            )
        finally:
            loop.close()

    def scan(self, domain: str, progress_cb=None, check_live: bool = False) -> Dict:

        if progress_cb:
            progress_cb(5, "queued")

        cmd = [
            "subfinder",
            "-d", domain,
            "-silent",
            "-t", "80",
            "-timeout", "12",
            "-sources", "crtsh,dnsdumpster,rapiddns,threatcrowd",
        ]

        try:
            if progress_cb:
                progress_cb(20, "enumerating")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                check=False
            )

            if progress_cb:
                progress_cb(75, "processing_results")

            if result.returncode != 0:
                msg = result.stderr.strip()[:200] or "subfinder execution failed"
                if progress_cb:
                    progress_cb(100, "failed")
                return {
                    "status": "error",
                    "message": msg,
                    "subdomains": [],
                    "count": 0
                }

            subdomains = sorted(set(
                line.strip()
                for line in result.stdout.splitlines()
                if line.strip() and '.' in line
            ))

            count = len(subdomains)

            response_data = {
                "status": "success",
                "count": count,
                "subdomains": subdomains,
                "message": f"Found {count} subdomains"
            }

            if check_live and subdomains:
                if progress_cb:
                    progress_cb(75, f"checking_live (0/{count})")

                live_subdomains = self._check_domains_live(subdomains, progress_cb)

                response_data['live_subdomains'] = live_subdomains
                response_data['live_count'] = len(live_subdomains)
                response_data['message'] = f"Found {count} subdomains ({len(live_subdomains)} live)"

            if progress_cb:
                if check_live and subdomains:
                    final_message = f"done ({count} found, {len(live_subdomains)} live)"
                else:
                    final_message = f"done ({count} found)"
                progress_cb(100, final_message)

            return response_data

        except subprocess.TimeoutExpired:
            if progress_cb:
                progress_cb(100, "timeout")
            return {
                "status": "error",
                "message": "Timeout (120s)",
                "subdomains": [],
                "count": 0
            }

        except Exception as e:
            if progress_cb:
                progress_cb(100, "error")
            return {
                "status": "error",
                "message": str(e),
                "subdomains": [],
                "count": 0
            }