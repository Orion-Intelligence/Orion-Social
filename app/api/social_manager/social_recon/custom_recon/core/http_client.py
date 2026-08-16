import json

from curl_cffi import requests as curl_requests

from api.social_manager.social_recon.constants.custom_recon_constants import HttpClientConstants, OnlineSearchConstants
from api.social_manager.social_recon.custom_recon.core.browser_pool import browser_pool
from api.social_manager.social_recon.normalizer import normalizer


def post(url: str, payload: str, headers: dict[str, str], max_bytes: int = HttpClientConstants.MAX_BYTES) -> tuple[int, str, str]:
    try:
        response = curl_requests.post(
            url,
            data=payload,
            headers=headers,
            impersonate=HttpClientConstants.IMPERSONATE,
            timeout=HttpClientConstants.TIMEOUT,
        )
        return response.status_code, (response.text or "")[:max_bytes], str(response.url)
    except Exception:
        return 0, "", url


def fetch(url: str, max_bytes: int = HttpClientConstants.MAX_BYTES, impersonate: str = HttpClientConstants.IMPERSONATE) -> tuple[int, str, str]:
    try:
        response = curl_requests.get(
            url,
            impersonate=impersonate,
            timeout=HttpClientConstants.TIMEOUT,
            allow_redirects=True,
        )
        return response.status_code, (response.text or "")[:max_bytes], str(response.url)
    except Exception:
        return 0, "", url


def browser_fetch(url: str, max_bytes: int = HttpClientConstants.MAX_BYTES) -> tuple[int, str, str]:
    return browser_pool().fetch(url, max_bytes)


def online_fetch(url: str, max_bytes: int = HttpClientConstants.MAX_BYTES) -> tuple[int, str, str]:
    from api.social_manager.scrapers.live_search_handler import live_search_handler

    target = normalizer.url(url)
    if target is None:
        return 0, "", url
    _value, host, path, _query = target
    query = OnlineSearchConstants.QUERY.format(target=f"{host}/{path}" if path else host)
    results: list = []
    for backend in OnlineSearchConstants.BACKENDS:
        try:
            results = live_search_handler()._ddgs_search("text", query, max_results=OnlineSearchConstants.MAX_RESULTS, backend=backend) or []
        except Exception:
            results = []
        if results:
            break
    matches = []
    for item in results:
        parts = normalizer.url(str(item.get("href") or ""))
        if not parts or not (parts[1] == host or parts[1].endswith(f".{host}")):
            continue
        found, wanted = parts[2].casefold(), path.casefold()
        if found == wanted or (wanted and found.startswith(f"{wanted}/")):
            matches.append({"href": item.get("href"), "title": item.get("title"), "body": item.get("body"), "exact": found == wanted})
    matches.sort(key=lambda match: not match["exact"])
    payload = {"query": query, "matches": matches, "results": len(results)}
    return 200, json.dumps(payload)[:max_bytes], str(matches[0]["href"]) if matches else url
