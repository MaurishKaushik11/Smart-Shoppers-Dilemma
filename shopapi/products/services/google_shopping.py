import asyncio
import re
from typing import List

import aiohttp
from user_agents import parse as parse_ua

from .schemas import ProductCard, ProductOffer


SEARCH_URL = "https://shopping.google.com/search?q={query}"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "upgrade-insecure-requests": "1",
    # Keep UA realistic for higher chance of consistent HTML
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
}


def _extract_text(pattern: str, html: str) -> List[str]:
    return re.findall(pattern, html, flags=re.IGNORECASE | re.DOTALL)


def _parse_price(text: str):
    # Extract numeric price and currency symbol
    m = re.search(r"([€£$])\s*([0-9]+(?:\.[0-9]{1,2})?)", text)
    if m:
        symbol, num = m.groups()
        currency = {"$": "USD", "€": "EUR", "£": "GBP"}.get(symbol, None)
        try:
            return float(num), currency
        except ValueError:
            return None, None
    return None, None


def _normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


async def fetch_google_shopping(query: str, session: aiohttp.ClientSession) -> List[ProductCard]:
    # Note: scraping Google directly may break; for production use APIs or headless browsers.
    from urllib.parse import quote_plus

    url = SEARCH_URL.format(query=quote_plus(query))
    async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as r:
        html = await r.text()

    cards: List[ProductCard] = []

    # Heuristic regexes for product cards in Google Shopping SERP HTML
    # Product blocks often have data-docid or sh-dgr__gr-auto headers.
    product_blocks = re.split(r'<div class="sh-dgr__content"', html)[1:]
    for block in product_blocks[:15]:  # limit to first N for speed
        name_match = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.DOTALL)
        name = _normalize_space(re.sub(r"<.*?>", " ", name_match.group(1))) if name_match else None
        if not name:
            continue

        # brand/weight heuristics from title
        brand = None
        total_weight = None
        # Try to capture things like '16 oz', '500 g', '1 lb', '12oz'
        weight_match = re.search(r"(\b\d+\s?(?:oz|g|kg|lb|lbs)\b)", name, re.IGNORECASE)
        if weight_match:
            total_weight = weight_match.group(1)

        # Brand heuristic: first token(s) before a hyphen or first capitalized word sequence
        brand_match = None
        try:
            import regex
            brand_match = regex.search(r"^(\p{Lu}[\p{L}\p{M}\p{N}]+(?:\s+\p{Lu}[\p{L}\p{M}\p{N}]+)*)\b", name)
        except ImportError:
            # fallback if regex module not installed
            brand_match = re.search(r"^([A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+)*)\b", name)

        if brand_match:
            brand = brand_match.group(1)

        # price heuristic
        price_match = re.search(r"[€£$]\s*[0-9]+(?:\.[0-9]{1,2})?", block)
        price_text = price_match.group(0) if price_match else None
        price_num, currency = _parse_price(price_text or "")

        # seller/link heuristic
        seller_match = re.search(r"From\s*([^<]+)", block)
        link_match = re.search(r'<a[^>]+href="(/shopping/product/[^"]+)"', block)

        offers = [
            ProductOffer(
                price=price_num,
                currency=currency,
                price_text=price_text,
                seller=_normalize_space(seller_match.group(1)) if seller_match else None,
                link=f"https://www.google.com{link_match.group(1)}" if link_match else None,
            )
        ] if price_text else []

        cards.append(
            ProductCard(
                name=name,
                brand=brand,
                total_weight=total_weight,
                offers=offers,
                source="google_shopping",
            )
        )

    return cards
