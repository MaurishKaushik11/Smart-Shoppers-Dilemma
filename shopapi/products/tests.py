import pytest
from django.test import AsyncClient
from unittest.mock import patch, AsyncMock
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

@pytest.mark.asyncio
async def test_search_products_success():
    client = AsyncClient()
    response = await client.get("/api/search?q=peanut butter")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert data["query"].lower() == "peanut butter"
    assert "results" in data
    assert isinstance(data["results"], list)

@pytest.mark.asyncio
async def test_search_products_missing_query():
    client = AsyncClient()
    response = await client.get("/api/search")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data

@pytest.mark.asyncio
@patch("shopapi.products.services.google_shopping.fetch_google_shopping", new_callable=AsyncMock)
async def test_search_products_google_fetch_error(mock_fetch):
    mock_fetch.side_effect = Exception("Fetch error")
    client = AsyncClient()
    response = await client.get("/api/search?q=test")
    assert response.status_code == 500
    data = response.json()
    assert "error" in data
    assert "Fetch error" in data["error"]

@pytest.mark.asyncio
@patch("shopapi.products.services.cache.cache")
async def test_cache_behavior(mock_cache):
    from shopapi.products.services.aggregator import aggregate_products
    mock_cache.get = AsyncMock(return_value=None)
    mock_cache.lock = AsyncMock()
    mock_cache.set = AsyncMock()
    # Simulate fetch_google_shopping returning empty list
    with patch("shopapi.products.services.google_shopping.fetch_google_shopping", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = []
        result = await aggregate_products("test")
        assert result.query == "test"
        assert result.results == []
        mock_cache.set.assert_called_once()
