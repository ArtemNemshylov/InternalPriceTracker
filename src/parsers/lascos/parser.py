import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser


class LascosParser(BaseParser):
    @staticmethod
    async def fetch_article(soup):
        try:
            article = soup.find("span", class_="p-model").text
            return article
        except Exception:
            return ""

    @staticmethod
    async def fetch_availability(soup):
        try:
            return True
        except Exception:
            return ""

    @staticmethod
    async def fetch_price(soup):
        try:
            price = soup.find("li", class_="product-price price-styled")
            if not price:
                return "", 0
            price = price.text.strip()
            price = int(price.replace(' ', '').replace('₴', ''))
            return price, 0
        except Exception:
            return "", 0


async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = LascosParser(
        browser_type="playwright",
        browser_config={
            "playwright": {
                "headless": False,
                "timeout": 45000
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
