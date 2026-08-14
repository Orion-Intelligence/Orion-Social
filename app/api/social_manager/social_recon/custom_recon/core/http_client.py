from curl_cffi import requests as curl_requests

from api.social_manager.social_recon.constants.custom_recon_constants import HttpClientConstants


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


def fetch(url: str, max_bytes: int = HttpClientConstants.MAX_BYTES) -> tuple[int, str, str]:
    try:
        response = curl_requests.get(
            url,
            impersonate=HttpClientConstants.IMPERSONATE,
            timeout=HttpClientConstants.TIMEOUT,
            allow_redirects=True,
        )
        return response.status_code, (response.text or "")[:max_bytes], str(response.url)
    except Exception:
        return 0, "", url
