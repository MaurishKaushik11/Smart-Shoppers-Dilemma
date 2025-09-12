# Overview

Smart Shopper API is a Django-based web service that aggregates product information from Google Shopping search results. The API provides a single endpoint that accepts search queries and returns structured product data including names, brands, prices, and weights. The system uses asynchronous processing to fetch data from multiple sources in parallel, with built-in caching to improve performance and reduce external API calls.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework Architecture
- **Django 4.2+** as the main web framework with async view support
- **Single API endpoint**: `GET /api/search?q=<product>` for product searches
- **Async views** using Django's native async capabilities for handling concurrent requests
- **JSON responses** with structured product data using Pydantic models

## Data Scraping Strategy
- **Playwright-based scraping** (migrated from aiohttp) for robust browser automation
- **Google Shopping** as the primary data source with HTML parsing
- **Extensible provider system** allowing easy addition of new data sources
- **Parallel fetching** using asyncio.gather() for concurrent data collection

## Caching Layer
- **In-memory TTL cache** with configurable expiration (default 5 minutes)
- **Per-key locking** to prevent duplicate requests for the same query
- **Async-safe implementation** using asyncio locks for thread safety
- **Production note**: Designed for Redis/Memcached replacement in production

## Data Processing Pipeline
- **Pydantic schemas** for data validation and serialization:
  - `ProductCard`: Main product structure with name, brand, weight, offers
  - `ProductOffer`: Individual pricing and seller information
  - `SearchResponse`: Complete API response wrapper
- **Text normalization** and regex-based parsing for extracting structured data
- **Price parsing** with multi-currency support (USD, EUR, GBP)

## Error Handling and Resilience
- **Exception propagation** with proper HTTP status codes (400, 500)
- **Timeout handling** for external requests (15-second timeout)
- **Graceful degradation** when parsing fails or sources are unavailable
- **Request validation** ensuring required query parameters are present

## Testing Infrastructure
- **Async unit tests** using pytest and Django's AsyncClient
- **Mock-based testing** for external service dependencies
- **Integration tests** for the complete API endpoint flow

# External Dependencies

## Core Framework Dependencies
- **Django 4.2+**: Web framework providing async view support and URL routing
- **Pydantic 2.8+**: Data validation and serialization with type hints
- **aiohttp 3.9+**: HTTP client for asynchronous requests (legacy, being phased out)
- **Playwright 1.40+**: Browser automation for robust HTML scraping

## Supporting Libraries
- **user-agents 2.2+**: User agent string parsing and generation for request headers
- **python-dotenv 1.0+**: Environment variable management for configuration
- **uvicorn**: ASGI server for development and production deployment
- **gunicorn**: WSGI/ASGI server for production deployment

## External Services
- **Google Shopping**: Primary data source accessed via web scraping
- **No database required**: Application is stateless with in-memory caching only
- **No authentication services**: Public API with no user management

## Development and Testing
- **pytest**: Async testing framework for unit and integration tests
- **Browser dependencies**: Chromium browser managed by Playwright for headless scraping

## Production Considerations
- **Redis/Memcached**: Recommended external cache replacement for scalability
- **Rate limiting services**: Not currently implemented but recommended for production
- **Monitoring/logging**: Basic error handling present, external monitoring recommended