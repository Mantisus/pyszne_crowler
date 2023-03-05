START_URL = "https://www.pyszne.pl/restauracja-dolnoslaskie"
DOMAIN_URL = "https://www.pyszne.pl"
API_URL = "https://cw-api.takeaway.com/api/v33/"

OUTPUT_FILE = "results.csv"


BASE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57"
    ),
    "Accept-Language": "uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "origin": "https://www.pyszne.pl",
    "referer": "https://www.pyszne.pl/",
}

NAVIGATE_HEADERS = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;" "q=0.8"
    ),
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

API_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pl",
    "x-country-code": "pl",
    "x-language-code": "pl",
}

NAVIGATE_CONCURRENTS = 10
API_CONCURRENTS = 1
