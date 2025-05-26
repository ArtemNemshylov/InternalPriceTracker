import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser
from src.parsers.utils import calculate_discount


class SesDermaParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    async def fetch_article(soup):
        try:
            article = soup.find("span", class_="sku")
            if article:
                return article.text.strip()
        except Exception:
            pass
        return ""

    async def fetch_price(self, soup):
        try:
            price_container = soup.find("p", class_="price")
            old_price_container = price_container.find("del")
            if old_price_container:
                old_price = old_price_container.find("bdi")
                price = price_container.find("ins").find("bdi")
                if old_price and price:
                    old_price = self._parse_price_text(old_price.text.strip())
                    price = self._parse_price_text(price.text.strip())
                    discount = calculate_discount(old_price, price)
                    return price, discount

            price = price_container.find("bdi")
            if price:
                price = self._parse_price_text(price.text.strip())
                return price, 0
        except Exception:
            pass
        return 0, 0

    @staticmethod
    async def fetch_availability(soup):
        try:
            if soup.find("p", class_="stock out-of-stock"):
                return False
        except Exception:
            pass
        return True

    @staticmethod
    def _parse_price_text(text: str) -> float:
        cleaned = text.replace('\xa0', '').replace('₴', '').replace(' ', '').replace(',', '')
        return float(cleaned)


async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = SesDermaParser(
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
