import asyncio
from shopapi.products.services.google_shopping_playwright import fetch_google_shopping_playwright

async def main():
    results = await fetch_google_shopping_playwright("365 WholeFoods Peanut Butter")
    print("Results:", results)
    print("Length:", len(results))

if __name__ == "__main__":
    asyncio.run(main())
