# TODO List for Smart Shopping Assistant Project

## 1. Fix Google Shopping Fetcher
- [x] Switch from aiohttp to Playwright for robust scraping (completed by user)
- [ ] Verify Playwright fetcher extracts product cards correctly (name, brand, price, total weight)
- [ ] Debug and fix any parsing issues in google_shopping_playwright.py

## 2. Update URL Routing
- [x] Add trailing slash to API URL pattern in shopapi/products/urls.py (completed by user)
- [ ] Confirm URL routing works properly

## 3. Implement and Run Unit Tests
- [x] Create test_google_shopping.py with async test for fetcher (completed by user)
- [ ] Run tests and ensure they pass with actual data
- [ ] Add tests for caching and aggregator if needed

## 4. Verify API Functionality
- [ ] Test the full API endpoint /api/search/ with sample queries
- [ ] Ensure structured JSON response with product cards
- [ ] Check caching reduces response time on repeated queries

## 5. Optimize for Speed and Scalability
- [ ] Confirm parallel fetching and async operations
- [ ] Test with multiple queries to ensure no bottlenecks

## 6. Prepare Deliverables
- [ ] Update README.md with setup/run instructions
- [ ] Update REPORT.md with approach, challenges, solutions, improvements
- [ ] Record demo video (<1 min) showing API in action
- [ ] Ensure code is ready for GitHub repo
