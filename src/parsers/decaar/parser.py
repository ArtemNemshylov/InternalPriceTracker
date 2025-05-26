import asyncio
from pathlib import Path
from src.parsers.base_parser import BaseParser


class DecaarParser(BaseParser):
    @staticmethod
    async def fetch_price(soup):
        try:
            price_container = soup.find("div", class_="info-buy")
            price = price_container.find("div", class_="price").text.strip()
            price = int(price.replace(' ', '').replace('грн', ''))
            return price, 0
        except Exception:
            return "", 0

    @staticmethod
    async def fetch_article(soup):
        try:
            return soup.find("div", class_="info-data-model").text.split(':')[1].strip()
        except Exception:
            return False

    @staticmethod
    async def fetch_availability(soup):
        try:
            container = soup.find("div", class_="info-data-stock")
            is_available = container.find("span").text.strip() == "У наявності"
            return is_available
        except Exception:
            return ""


async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"

    parser = DecaarParser(
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
