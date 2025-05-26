import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser


class Name(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def fetch_price(self, soup):
        pass

    async def fetch_availability(self, soup):
        pass

    async def fetch_article(self, soup):
        pass

async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = Name(
        browser_type="playwright",
        browser_config={
            "playwright": {
                "headless": True,
                "timeout": 30000
            }
        }
    )
    try:
        urls = links_path.read_text(encoding="utf-8").splitlines()
        products = await parser.parse(urls)
        return products
    finally:
        await parser.close()

if __name__ == "__main__":
    asyncio.run(main())
