import asyncio
from typing import List
import aiohttp

from .cache import cache
from .schemas import SearchResponse, ProductCard
from .google_shopping_playwright import fetch_google_shopping_playwright as fetch_google_shopping


async def aggregate_products(query: str, ttl_seconds: int = 300) -> SearchResponse:
    key = f"search:{query.lower().strip()}"

    # Check cache
    cached = await cache.get(key)
    if cached:
        return cached

    # Ensure only one fetch per key at a time
    lock = await cache.lock(key)
    async with lock:
        cached2 = await cache.get(key)
        if cached2:
            return cached2

        # Run multiple sources in parallel; currently only Google, but easy to extend
        tasks = [
            fetch_google_shopping(query),
            # add more providers here
        ]
        results_lists: List[List[ProductCard]] = await asyncio.gather(*tasks, return_exceptions=False)

        flat: List[ProductCard] = []
        sources_used: List[str] = []
        for lst in results_lists:
            if not lst:
                continue
            flat.extend(lst)
            sources_used.extend({card.source for card in lst if card.source})

        response = SearchResponse(query=query, results=flat, sources_used=sorted(set(sources_used)))
        await cache.set(key, response, ttl=ttl_seconds)
        return response