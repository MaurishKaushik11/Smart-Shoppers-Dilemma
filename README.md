# Smart Shopper API

Fast, async Django API to fetch product cards (name, brand, price, total weight) from Google Shopping-like results.

## Features
- **Async pipeline** using `aiohttp`
- **Parallel providers** (Google Shopping included; easy to add more)
- **In-memory TTL cache** to reduce repeated work
- **Django endpoint**: `GET /api/search?q=<product>`

## Quick Start
1. Python 3.10+ required.
2. Create and activate venv, install deps:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run server:
   ```bash
   cd shopapi
   python manage.py runserver 0.0.0.0:8000
   ```
4. Test API:
   - Browser/cURL: `http://localhost:8000/api/search?q=365%20WholeFoods%20Peanut%20Butter`

Notes:
- Scraping HTML can be flaky. For production use, consider official APIs or headless browsers and external cache (Redis).
- This demo includes simple parsing heuristics.

## Project Structure
- `shopapi/config` — Django project
- `shopapi/products` — app and API
- `shopapi/products/services` — async services (cache, google fetcher, aggregator, schemas)

## Extend Providers
- Add a new async function returning `List[ProductCard]` in `products/services/your_source.py`.
- Append it to the `tasks` list in `aggregator.py`.

## Demo
- Record a <1 min screen capture hitting the endpoint and showing JSON.

## License
MIT