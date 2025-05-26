import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser


class ChristinaCosmeticsParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def fetch_price(self, soup):
        try:
            container = soup.find("div", class_="product-prices flex")
            price_block = container.find("li", class_="price-big")

            main_price_tag = price_block.find("span", class_="h2")
            if not main_price_tag:
                return 0, 0

            main_price = float(main_price_tag.text.strip().replace("грн", "").replace(" ", "").replace(",", "."))

            old_price_tag = price_block.find("span", style=lambda s: s and "line-through" in s)
            if old_price_tag:
                old_price = float(old_price_tag.text.strip().replace("грн", "").replace(" ", "").replace(",", "."))
                discount = int(round((old_price - main_price) / old_price * 100))
            else:
                discount = 0

            return int(main_price), discount
        except Exception as e:
            return 0, 0

    async def fetch_availability(self, soup):
        if soup.find("button", class_="btn btn-primary btn-new btn-medium btn-block"):
            return True
        return False

    async def fetch_article(self, soup):
        try:
            article = soup.find("div", class_="product-sku").find("span").text.strip()
            return article
        except Exception:
            return ""

async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = ChristinaCosmeticsParser(
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