import re


class EmailExtractorConstants:
    HOLEHE_TIMEOUT = 120


class UsernameExtractorConstants:
    SITE_TIMEOUT = 5
    SEARCH_DEADLINE = 540
    MAX_CONNECTIONS = 60
    SEARCH_ENDPOINT = re.compile(
        r"/search(?:/|\.php|$)|/users/filter\b|[?&](?:q|query|keywords?|terms?|search|author)=",
        re.IGNORECASE,
    )
