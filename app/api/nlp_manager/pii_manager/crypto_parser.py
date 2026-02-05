import re
from functools import lru_cache
from coinaddrvalidator import currency, validate

_GENERIC_TOKEN_RE = re.compile(r"\b[0-9A-Za-z]{25,64}\b")

_BASE58_CHARS = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
_BECH32_CHARS = set("023456789acdefghjklmnpqrstuvwxyz")
_STELLAR_BASE32 = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
_HEX_CHARS = set("0123456789abcdefABCDEF")

def _all_base58(s: str) -> bool:
    return all(c in _BASE58_CHARS for c in s)

def _all_bech32(s: str) -> bool:
    return all(c in _BECH32_CHARS for c in s)

def _all_hex(s: str) -> bool:
    return all(c in _HEX_CHARS for c in s)

def _all_stellar32(s: str) -> bool:
    return all(c in _STELLAR_BASE32 for c in s)

def _get_all_coins() -> tuple[str, ...]:
    return tuple(sorted({c.ticker for c in currency.Currencies.instances.values()}))

_ALL_COINS = _get_all_coins()

_PRIORITY_ORDER = (
    "btc", "eth", "ltc", "bch", "xrp", "doge", "trx", "ada", "xlm",
    "zec", "dash", "etc", "neo", "bsv", "xmr",
)
_PRIORITY_COINS = tuple(c for c in _PRIORITY_ORDER if c in _ALL_COINS)
_REMAINING_COINS = tuple(c for c in _ALL_COINS if c not in _PRIORITY_COINS)

def _hint_candidates(token: str) -> tuple[str, ...]:
    t = token
    tl = t.lower()
    n = len(t)
    if tl.startswith("0x") and n == 42 and _all_hex(t[2:]):
        return ("eth",)
    if tl.startswith(("bc1", "tb1", "bcrt1")) and 14 <= n <= 90 and _all_bech32(tl[3:]):
        return ("btc",)
    if tl.startswith("ltc1") and 14 <= n <= 90 and _all_bech32(tl[4:]):
        return ("ltc",)
    if tl.startswith("addr1") and n >= 30 and _all_bech32(tl[5:]):
        return ("ada",)
    if t.startswith("r") and 25 <= n <= 35 and _all_base58(t):
        return ("xrp",)
    if t and t[0] in ("T", "t") and 30 <= n <= 36 and _all_base58(t):
        return ("trx",)
    if t.startswith("G") and n == 56 and _all_stellar32(t):
        return ("xlm",)
    if t[0:1] in {"1", "3"} and 26 <= n <= 35 and _all_base58(t):
        return tuple(c for c in ("btc", "ltc", "dash", "zec", "doge", "bch") if c in _ALL_COINS)
    return ()

class crypto_parser:
    @staticmethod
    def _hinted_coin_order(token: str) -> tuple[str, ...]:
        t = token.lower()
        if t.startswith("0x") and len(t) == 42:
            return ("eth",) + _PRIORITY_COINS + _REMAINING_COINS
        if t.startswith(("1", "3", "bc1")):
            return ("btc",) + _PRIORITY_COINS + _REMAINING_COINS
        if t.startswith("r") and 25 <= len(t) <= 35:
            return ("xrp",) + _PRIORITY_COINS + _REMAINING_COINS
        if t.startswith(("t", "T")) and 30 <= len(t) <= 36:
            return ("trx",) + _PRIORITY_COINS + _REMAINING_COINS
        return _PRIORITY_COINS + _REMAINING_COINS

    @staticmethod
    @lru_cache(maxsize=100_000)
    def _validate_cached(coin: str, addr: str) -> bool:
        try:
            return bool(validate(coin, addr).valid)
        except Exception:
            return False

    @staticmethod
    def _check_one_token(token: str) -> str | None:
        candidates = _hint_candidates(token)
        if candidates:
            for coin in candidates:
                if crypto_parser._validate_cached(coin, token):
                    return token
            return None
        for coin in crypto_parser._hinted_coin_order(token)[:6]:
            if crypto_parser._validate_cached(coin, token):
                return token
        return None

    @staticmethod
    def extract_valid_addresses(text: str, max_workers: int | None = None) -> list[str]:
        tokens = set(_GENERIC_TOKEN_RE.findall(text))
        if not tokens:
            return []
        results: set[str] = set()
        for tok in tokens:
            ok = crypto_parser._check_one_token(tok)
            if ok:
                results.add(ok)
        return sorted(results)
