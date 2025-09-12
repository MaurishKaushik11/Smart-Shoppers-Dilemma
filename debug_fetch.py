import asyncio
import aiohttp

SEARCH_URL = "https://shopping.google.com/search?q={query}"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "upgrade-insecure-requests": "1",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
}

async def fetch_html(query):
    from urllib.parse import quote_plus
    url = SEARCH_URL.format(query=quote_plus(query))
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as r:
            html = await r.text()
    return html

if __name__ == "__main__":
    html = asyncio.run(fetch_html("365 WholeFoods Peanut Butter"))
    print(html[:2000])  # print first 2000 chars
