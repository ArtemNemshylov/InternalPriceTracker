import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser


class YudinaParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def fetch_price(self, soup):
        try:
            container = soup.find("span", class_="woocommerce-Price-amount amount")
            price_text = container.find("bdi").text.strip().replace(" ", "")
            price_cleaned = price_text.replace(",", ".").replace("₴", "")
            return int(float(price_cleaned)), 0
        except Exception:
            return 0, 0

    async def fetch_availability(self, soup):
        if soup.find("button", class_="single_add_to_cart_button button alt"):
            return True
        return False

    async def fetch_article(self, soup):
        try:
            article = soup.find("span", class_="sku qodef-woo-meta-value").text.strip()
            return article
        except Exception:
            return ""


async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = YudinaParser(
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