import asyncio
from pathlib import Path
import re
from src.parsers.base_parser import BaseParser


class PielCosmeticsParser(BaseParser):
    @staticmethod
    async def fetch_article(soup):
        article_container = soup.find("div", class_="wrapper__goods-basic_info-info-vendor_code")
        article = article_container.find("p").text.split(':')[1].strip()
        return article

    @staticmethod
    async def fetch_availability(soup):
        button_container = soup.find("div", class_="wrapper__goods-basic_info-info-descriptions")
        if button_container.find("button", class_="bxm-notify-when-available--button"):
            return False
        return True

    @staticmethod
    async def fetch_price(soup):
        container = soup.find("div", class_="wrapper__goods-basic_info-info-price")
        if not container:
            return 0, 0

        price_stock = container.find("p", class_="price-stock")
        if price_stock and price_stock.text.strip():
            price_text = price_stock.text.strip()
        else:
            price_spans = container.find("p", class_="price").find_all("span")
            price_text = price_spans[-1].text.strip() if price_spans else "0"

        saving_block = container.find("p", class_="saving")
        if saving_block:
            discount_span = saving_block.find("span")
            discount_text = discount_span.text.strip() if discount_span else "0%"
            discount = int(re.sub(r"[^\d]", "", discount_text)) if discount_text else 0
        else:
            discount = 0

        clean_price = re.sub(r"[^\d]", "", price_text)
        return int(clean_price), discount

async def main():
    parser = PielCosmeticsParser(
        browser_type="playwright",
        browser_config={
            "playwright": {
                "headless": True,
                "timeout": 4500
            }
        }
    )
    try:
        urls = Path("links.txt").read_text(encoding="utf-8").splitlines()
        products = await parser.parse(urls)
        for product in products:
            print(product.article, product.price, product.available, product.discount)
    finally:
        await parser.close()


if __name__ == "__main__":
    asyncio.run(main())