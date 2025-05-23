import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser


class LascosParser(BaseParser):
    @staticmethod
    async def fetch_article(soup):
        article = soup.find("span", class_="p-model").text
        return article

    @staticmethod
    async def fetch_availability(soup):
        return True

    @staticmethod
    async def fetch_price(soup):
        price = soup.find("li", class_="product-price price-styled")
        if not price:
            return 0, 0
        price = price.text.strip()
        price = int(price.replace(' ', '').replace('₴', ''))
        return price, 0


async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = LascosParser(
        browser_type="playwright",
        browser_config={
            "playwright": {
                "headless": False,
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