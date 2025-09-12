import asyncio
import unittest
import aiohttp
from django.test import SimpleTestCase
import asyncio

from products.services.google_shopping_playwright import fetch_google_shopping_playwright as fetch_google_shopping

class TestGoogleShoppingFetcher(SimpleTestCase):
    async def test_fetch_google_shopping(self):
        results = await fetch_google_shopping("365 WholeFoods Peanut Butter")
        print(results)
        self.assertTrue(len(results) > 0, "Expected at least one product card")

class TestGoogleShoppingFetcher(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_google_shopping(self):
        results = await fetch_google_shopping("365 WholeFoods Peanut Butter")
        print(results)
        self.assertTrue(len(results) > 0, "Expected at least one product card")

if __name__ == "__main__":
    unittest.main()
