import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser


class JDAParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def fetch_price(self, soup):
        try:
            price_meta = soup.find("meta", itemprop="price")
            price = int(price_meta["content"]) if price_meta else 0

            old_price_div = soup.find("div", class_="product-price__old-price")
            if old_price_div:
                old_price_text = old_price_div.text.strip().replace(" ", "").replace("грн", "")
                old_price = int(old_price_text)
                discount = 100 - round(price / old_price * 100)
                return price, discount

            return price, 0
        except Exception:
            return 0, 0


    async def fetch_availability(self, soup):
        try:
            container = soup.find("div", class_="product-header__availability")
            return True
        except Exception:
            return False


    async def fetch_article(self, soup):
        try:
            container = soup.find("div", class_="product-header__code")
            article = container.text.replace("Артикул: ", "").strip()
            return article
        except Exception:
            return ""


async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = JDAParser(
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
        for product in products:
            print(product.article, product.price, product.available, product.discount)
        return products
    finally:
        await parser.close()


if __name__ == "__main__":
    asyncio.run(main())
