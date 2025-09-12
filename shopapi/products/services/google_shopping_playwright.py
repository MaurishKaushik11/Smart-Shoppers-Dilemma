import asyncio
from typing import List
from urllib.parse import quote_plus

from playwright.async_api import async_playwright

from .schemas import ProductCard, ProductOffer


SEARCH_URL = "https://shopping.google.com/search?q={query}"


def _normalize_space(s: str) -> str:
    import re
    return re.sub(r"\s+", " ", s).strip()


def _parse_price(text: str):
    import re
    m = re.search(r"([€£$])\s*([0-9]+(?:\.[0-9]{1,2})?)", text)
    if m:
        symbol, num = m.groups()
        currency = {"$": "USD", "€": "EUR", "£": "GBP"}.get(symbol, None)
        try:
            return float(num), currency
        except ValueError:
            return None, None
    return None, None


async def fetch_google_shopping_playwright(query: str) -> List[ProductCard]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = SEARCH_URL.format(query=quote_plus(query))
        await page.goto(url, timeout=15000)
        content = await page.content()
        await browser.close()

    import re
    cards: List[ProductCard] = []

    product_blocks = re.split(r'<div class="sh-dgr__content"', content)[1:]
    for block in product_blocks[:15]:
        name_match = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.DOTALL)
        name = _normalize_space(re.sub(r"<.*?>", " ", name_match.group(1))) if name_match else None
        if not name:
            continue

        brand = None
        total_weight = None
        weight_match = re.search(r"(\b\d+\s?(?:oz|g|kg|lb|lbs)\b)", name, re.IGNORECASE)
        if weight_match:
            total_weight = weight_match.group(1)

        brand_match = re.search(r"^([A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+)*)\b", name)
        if brand_match:
            brand = brand_match.group(1)

        price_match = re.search(r"[€£$]\s*[0-9]+(?:\.[0-9]{1,2})?", block)
        price_text = price_match.group(0) if price_match else None
        price_num, currency = _parse_price(price_text or "")

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
                source="google_shopping_playwright",
            )
        )

    return cards
