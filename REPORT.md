# Approach, Challenges, Solutions, Improvements

## Approach
- Built a minimal **Django** project with an **async view** (`/api/search`) that orchestrates an async aggregation pipeline.
- Implemented **parallel fetching** using `aiohttp` for Google Shopping SERP HTML, with **in-memory TTL caching** to reduce latency on repeated queries.
- Defined **Pydantic schemas** to ensure structured, typed responses.

## Challenges
- **Unstable HTML structure** of Google results; selectors can change and differ by locale/device.
- **Rate limiting / Bot detection** by Google for frequent requests.
- **Parsing prices/weights** reliably from unstructured text.

## Solutions
- Heuristic-based parsing via regex for names, weights, prices; tolerant fallbacks.
- Realistic headers and limited parallelism to reduce detection.
- **Caching** responses for a few minutes to avoid redundant calls.

## Improvements
- Use a **headless browser** (Playwright) for more robust DOM extraction.
- Add **Redis** cache and request deduplication across processes.
- Integrate additional providers/APIs to improve recall.
- Add **rate limiting**, **retry with backoff**, and **structured logging/metrics**.
- Enhance extraction with **ML/NLP** for brand/weight normalization.