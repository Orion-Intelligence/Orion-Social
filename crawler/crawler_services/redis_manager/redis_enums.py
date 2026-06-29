import os
from enum import Enum


class REDIS_CONNECTIONS:
    S_DATABASE_IP = os.getenv("REDIS_HOST") or os.getenv("REDIS_SERVER") or ("redis_server" if os.path.exists("/app") else "localhost")
    S_DATABASE_PORT = int(os.getenv("REDIS_PORT", "6379"))
    S_DATABASE_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    _v = 27
    _redis_key_version = f"V{_v}_"


class REDIS_KEYS:
    RAW_HTML_SCORE = f"RAW_HTML_SCORE_{REDIS_CONNECTIONS._redis_key_version}"
    RAW_HTML_CODE = f"RAW_HTML_CODE_{REDIS_CONNECTIONS._redis_key_version}"
    LEAK_PARSED = f"LEAK_PARSED_CODE_{REDIS_CONNECTIONS._redis_key_version}"
    HOST_FAILURE_COUNT = f"HOST_FAIL_{REDIS_CONNECTIONS._redis_key_version}"
    HOST_LOW_YIELD_COUNT = f"LOW_YIELD_{REDIS_CONNECTIONS._redis_key_version}"
    UNIQIE_CRAWLER_RUNNING = f"UNIQIE_CRAWLER_RUNNING_{REDIS_CONNECTIONS._redis_key_version}"
    S_URL_TIMEOUT = f"S_URL_TIMEOUT_TEST_{REDIS_CONNECTIONS._redis_key_version}"


class CUSTOM_SCRIPT_REDIS_KEYS(Enum):
    URL_PARSED = f"URL_PARSED_{REDIS_CONNECTIONS._redis_key_version}"
    TELEGRAM_CHANNEL_PARSED = f"TELEGRAM_CHANNEL_PARSED_{REDIS_CONNECTIONS._redis_key_version}"
    S_TWITTER_CHANNEL = f"S_TWITTER_CHANNEL_{REDIS_CONNECTIONS._redis_key_version}"


class REDIS_COMMANDS:
    S_SET_BOOL = 1
    S_GET_BOOL = 2
    S_SET_INT = 3
    S_GET_INT = 4
    S_SET_STRING = 5
    S_GET_STRING = 6
    S_SET_LIST = 7
    S_GET_LIST = 8
    S_GET_KEYS = 9
    S_GET_FLOAT = 10
    S_SET_FLOAT = 11
    S_FLUSH_ALL = 12
    S_ACQUIRE_LOCK = 13
    S_RELEASE_LOCK = 14
